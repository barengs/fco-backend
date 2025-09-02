from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User

# Custom permission definitions
CUSTOM_PERMISSIONS = {
    'user_management': {
        'view_user_profile': 'Can view user profiles',
        'edit_user_profile': 'Can edit user profiles',
        'delete_user': 'Can delete users',
        'manage_user_roles': 'Can manage user roles',
    },
    'ship_management': {
        'view_ship': 'Can view ship information',
        'edit_ship': 'Can edit ship information',
        'delete_ship': 'Can delete ship information',
        'assign_captain': 'Can assign captain to ship',
    },
    'fishing_operations': {
        'view_fishing_data': 'Can view fishing data',
        'edit_fishing_data': 'Can edit fishing data',
        'delete_fishing_data': 'Can delete fishing data',
        'approve_fishing_report': 'Can approve fishing reports',
    }
}

def create_custom_permissions():
    """
    Create custom permissions for the application
    """
    # Get the content type for the User model
    content_type = ContentType.objects.get_for_model(User)
    
    # Create custom permissions
    for category, permissions in CUSTOM_PERMISSIONS.items():
        for codename, name in permissions.items():
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type,
            )

def assign_permission_to_user(user, permission_codename):
    """
    Assign a specific permission to a user
    """
    try:
        permission = Permission.objects.get(codename=permission_codename)
        user.user_permissions.add(permission)
        return True
    except Exception:
        return False

def assign_permission_to_group(group_name, permission_codename):
    """
    Assign a specific permission to a group
    """
    from django.contrib.auth.models import Group
    
    try:
        group = Group.objects.get(name=group_name)
        permission = Permission.objects.get(codename=permission_codename)
        group.permissions.add(permission)
        return True
    except Exception:
        return False

def user_has_permission(user, permission_codename):
    """
    Check if a user has a specific permission
    """
    return user.has_perm(permission_codename)