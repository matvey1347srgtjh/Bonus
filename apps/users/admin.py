from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from .models import Employee, WorkPlan
from apps.rewards.services import RewardService
from apps.rewards.models import RewardSetting

admin.site.unregister(Group)
admin.site.register(RewardSetting)
admin.site.register(WorkPlan)

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = (
            'username', 'first_name', 'last_name', 'middle_name', 
            'email', 'department', 'position', 'date_of_birth'
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
        'position', 'needs_password_change', 'profile_bonus_received'
    )
    actions = ['make_employee_official']
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
    
    @admin.action(description="Принять в штат (начислить бонус ментору)")
    def make_employee_official(self, request, queryset):
        success_count = 0
        for obj in queryset:
            if RewardService.approve_trial_period(obj):
                success_count += 1
        
        self.message_user(request, f"Успешно: {success_count} сотрудников приняты, менторы вознаграждены.")