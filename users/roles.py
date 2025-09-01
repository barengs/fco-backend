from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from .models import User

def create_default_roles():
    """
    Create default roles/groups with appropriate permissions
    """
    # Create roles/groups
    roles_permissions = {
        'admin': {
            'permissions': [
                # All permissions for admin
            ],
            'description': 'Administrator with full access'
        },
        'ship_owner': {
            'permissions': [
                # Specific permissions for ship owners
                'view_user',
                'change_user',
            ],
            'description': 'Ship owner with limited access'
        },
        'captain': {
            'permissions': [
                # Specific permissions for captains
                'view_user',
                'change_user',
            ],
            'description': 'Captain with limited access'
        }
    }
    
    for role_name, role_data in roles_permissions.items():
        # Create or get the group
        group, created = Group.objects.get_or_create(name=role_name)
        
        # Add permissions to the group
        for perm_codename in role_data['permissions']:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                group.permissions.add(permission)
            except ObjectDoesNotExist:
                # Handle case where permission doesn't exist
                pass
        
        # If this is a new group, save the description
        if created:
            # You could save the description in a custom model if needed
            pass

def assign_user_to_role(user, role_name):
    """
    Assign a user to a specific role
    """
    try:
        group = Group.objects.get(name=role_name)
        user.groups.add(group)
        return True
    except ObjectDoesNotExist:
        return False

def get_user_roles(user):
    """
    Get all roles assigned to a user
    """
    return user.groups.all()

def is_user_in_role(user, role_name):
    """
    Check if a user is in a specific role
    """
    return user.groups.filter(name=role_name).exists()