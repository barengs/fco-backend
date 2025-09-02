from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ShipOwnerProfile, CaptainProfile, AdminProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_user_role', 'is_staff', 'get_roles')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('username', 'email')
    ordering = ('username',)

    @admin.display(description='User Role')
    def get_user_role(self, obj):
        roles = obj.role_names
        if 'ship_owner' in roles:
            return 'Ship Owner'
        elif 'captain' in roles:
            return 'Captain'
        elif 'admin' in roles:
            return 'Admin'
        return 'Unknown'

    @admin.display(description='Roles')
    def get_roles(self, obj):
        return ", ".join(obj.role_names)

class ShipOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'owner_type', 'company_name', 'tax_id', 'created_at')
    list_filter = ('owner_type', 'created_at')
    search_fields = ('user__username', 'company_name', 'tax_id')
    readonly_fields = ('created_at', 'updated_at')

class CaptainProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'years_of_experience', 'created_at')
    list_filter = ('years_of_experience', 'created_at')
    search_fields = ('user__username', 'license_number')
    readonly_fields = ('created_at', 'updated_at')

class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'position', 'institution', 'created_at')
    list_filter = ('department', 'position', 'created_at')
    search_fields = ('user__username', 'employee_id', 'institution')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(User, CustomUserAdmin)
admin.site.register(ShipOwnerProfile, ShipOwnerProfileAdmin)
admin.site.register(CaptainProfile, CaptainProfileAdmin)
admin.site.register(AdminProfile, AdminProfileAdmin)