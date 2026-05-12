from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.db import transaction
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Employee, WorkPlan
from apps.rewards.services import RewardService
from apps.rewards.models import RewardSetting
from apps.wallets.models import Transaction as WalletTransaction

admin.site.unregister(Group)
admin.site.register(RewardSetting)
admin.site.register(WorkPlan)

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = (
            'username', 'email', 'department', 'is_intern',
            'password', 'needs_password_change'
        )
        import_id_fields = ('username',)

    def before_import_row(self, row, **kwargs):
        row['password'] = make_password('IRZ_Bonus_2026')
        row['needs_password_change'] = True

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = EmployeeResource
    list_display = (
        'username', 'last_name', 'first_name', 'department', 
        'position', 'get_balance', 'needs_password_change', 'profile_bonus_received'
    )
    actions = ['make_employee_official', 'bonus_1000']
    
    list_filter = ('department', 'is_staff', 'is_superuser', 'needs_password_change')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        ('Информация ИРЗ', {'fields': ('department', 'position', 'hired_at', 'phone', 'date_of_birth')}),
        ('Статусы и безопасность', {
            'fields': ('needs_password_change', 'profile_bonus_received', 'is_intern', 'trial_passed', 'mentor')
        }),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Информация ИРЗ', {'fields': ('middle_name', 'department', 'position', 'hired_at', 'phone')}),
    )

    def get_balance(self, obj):
        return obj.wallet.balance if hasattr(obj, 'wallet') else 0
    get_balance.short_description = 'Баланс (б.)'
    
    @admin.action(description="Принять в штат (начислить бонус ментору)")
    def make_employee_official(self, request, queryset):
        success_count = 0
        for obj in queryset:
            if RewardService.approve_trial_period(obj):
                success_count += 1
        self.message_user(request, f"Успешно: {success_count} сотрудников приняты, менторы вознаграждены.")

    @admin.action(description="Начислить 1000 баллов выбранным")
    def bonus_1000(self, request, queryset):
        success_count = 0
        try:
            with transaction.atomic():
                for employee in queryset:
                    wallet = getattr(employee, 'wallet', None)
                    if wallet:
                        wallet.balance += 1000
                        wallet.save()
                        
                        WalletTransaction.objects.create(
                            wallet=wallet,
                            amount=1000,
                            type='IN',
                            reason="Поощрение от администрации"
                        )
                        success_count += 1
            
            self.message_user(request, f"Начислено по 1000 баллов {success_count} сотрудникам.")
        except Exception as e:
            self.message_user(request, f"Ошибка: {e}", level=messages.ERROR)