from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, WorkPlan
from django.contrib.auth.models import Group
from apps.rewards.services import RewardService
from apps.rewards.models import RewardSetting

admin.site.unregister(Group)
admin.site.register(RewardSetting)
admin.site.register(WorkPlan)

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'department', 'position', 'is_staff')
    actions = ['make_employee_official']
    list_filter = ('department', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        ('Информация ИРЗ', {'fields': ('department', 'position', 'hired_at', 'phone', 'date_of_birth')}),
        ('Статусы бонусов', {'fields': ('profile_bonus_received', 'is_intern', 'trial_passed', 'mentor')}),
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