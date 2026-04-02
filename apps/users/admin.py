from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'department', 'position', 'is_staff')
    
    list_filter = ('department', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        ('Информация ИРЗ', {'fields': ('department', 'position', 'hired_at', 'phone', 'date_of_birth')}),
        ('Статусы бонусов', {'fields': ('profile_bonus_received', 'is_intern', 'trial_passed', 'mentor')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Информация ИРЗ', {'fields': ('middle_name', 'department', 'position', 'hired_at', 'phone')}),
    )