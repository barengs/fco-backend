from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from .roles import assign_user_to_role, is_user_in_role
from .permissions import assign_permission_to_user, user_has_permission

class RoleManagementService:
    """
    Service class to handle role and permission management
    """
    
    @staticmethod
    def create_role(role_name, description="", permissions=None):
        """
        Create a new role (group) with optional permissions
        """
        group, created = Group.objects.get_or_create(name=role_name)
        
        if not created and description:
            # Update description if needed (would require a custom model)
            pass
            
        if permissions:
            for perm_codename in permissions:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except ObjectDoesNotExist:
                    # Log error or handle appropriately
                    pass
                    
        return group, created
    
    @staticmethod
    def delete_role(role_name):
        """
        Delete a role (group)
        """
        try:
            group = Group.objects.get(name=role_name)
            group.delete()
            return True
        except ObjectDoesNotExist:
            return False
    
    @staticmethod
    def assign_user_to_role(user, role_name):
        """
        Assign a user to a specific role
        """
        return assign_user_to_role(user, role_name)
    
    @staticmethod
    def remove_user_from_role(user, role_name):
        """
        Remove a user from a specific role
        """
        try:
            group = Group.objects.get(name=role_name)
            user.groups.remove(group)
            return True
        except ObjectDoesNotExist:
            return False
    
    @staticmethod
    def get_user_roles(user):
        """
        Get all roles assigned to a user
        """
        return user.groups.all()
    
    @staticmethod
    def is_user_in_role(user, role_name):
        """
        Check if a user is in a specific role
        """
        return is_user_in_role(user, role_name)
    
    @staticmethod
    def assign_permission_to_user(user, permission_codename):
        """
        Assign a specific permission directly to a user
        """
        return assign_permission_to_user(user, permission_codename)
    
    @staticmethod
    def remove_permission_from_user(user, permission_codename):
        """
        Remove a specific permission from a user
        """
        try:
            permission = Permission.objects.get(codename=permission_codename)
            user.user_permissions.remove(permission)
            return True
        except ObjectDoesNotExist:
            return False
    
    @staticmethod
    def user_has_permission(user, permission_codename):
        """
        Check if a user has a specific permission
        """
        return user_has_permission(user, permission_codename)
    
    @staticmethod
    def get_role_permissions(role_name):
        """
        Get all permissions for a specific role
        """
        try:
            group = Group.objects.get(name=role_name)
            return group.permissions.all()
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def add_permission_to_role(role_name, permission_codename):
        """
        Add a permission to a role
        """
        try:
            group = Group.objects.get(name=role_name)
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.add(permission)
            return True
        except ObjectDoesNotExist:
            return False
    
    @staticmethod
    def remove_permission_from_role(role_name, permission_codename):
        """
        Remove a permission from a role
        """
        try:
            group = Group.objects.get(name=role_name)
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.remove(permission)
            return True
        except ObjectDoesNotExist:
            return False