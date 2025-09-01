from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from typing import Any

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'ship_registration_number', 'is_staff', 'get_roles')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_type', 'ship_registration_number', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'ship_registration_number', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'ship_registration_number')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    def get_roles(self, obj: Any) -> str:
        return ", ".join([group.name for group in obj.groups.all()])
    
    # Type-safe way to set the short_description
    get_roles.short_description = 'Roles'  # type: ignore[attr-defined]

admin.site.register(User, UserAdmin)