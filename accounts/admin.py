from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'mobile_number', 'job_title', 'department', 'is_staff', 'is_admin', 'is_superuser']
    list_filter = ['email', 'is_staff', 'is_admin', 'is_superuser', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile_number', 'job_title', 'department')}),
        ('Permissions', {'fields': ('is_staff', 'is_admin', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'mobile_number', 'job_title', 'department')
        }),
    )
    search_fields = ['email']
    ordering = ['email']

admin.site.register(CustomUser, CustomUserAdmin)