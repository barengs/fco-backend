# Role Management System Documentation

## Overview

This role management system provides a comprehensive solution for managing user roles and permissions in the Fish Chain Optimization application. It combines Django's built-in authentication and authorization system with custom role management features.

## Components

### 1. Roles Module (`users/roles.py`)

Manages the creation and assignment of roles (Django Groups) to users.

#### Key Functions:

- `create_default_roles()` - Creates default roles with appropriate permissions
- `assign_user_to_role(user, role_name)` - Assigns a user to a specific role
- `get_user_roles(user)` - Gets all roles assigned to a user
- `is_user_in_role(user, role_name)` - Checks if a user is in a specific role

### 2. Permissions Module (`users/permissions.py`)

Manages custom permissions for the application.

#### Key Functions:

- `create_custom_permissions()` - Creates custom permissions for the application
- `assign_permission_to_user(user, permission_codename)` - Assigns a specific permission to a user
- `assign_permission_to_group(group_name, permission_codename)` - Assigns a specific permission to a group
- `user_has_permission(user, permission_codename)` - Checks if a user has a specific permission

### 3. Services Module (`users/services.py`)

Provides a service layer for role and permission management operations.

#### Key Classes:

- `RoleManagementService` - Service class with static methods for role/permission operations

### 4. Decorators (`users/decorators.py`)

Provides decorators for role-based access control in views.

#### Key Decorators:

- `@role_required(roles)` - Restricts access to users with specific roles
- `@permission_required(permission)` - Restricts access to users with specific permissions
- `@role_or_permission_required(roles, permissions)` - Restricts access to users with specific roles OR permissions

## API Endpoints

### Role Management

- `GET /api/users/roles/` - List all roles
- `POST /api/users/roles/create/` - Create a new role
- `DELETE /api/users/roles/<role_name>/delete/` - Delete a role
- `POST /api/users/roles/assign/` - Assign a user to a role
- `POST /api/users/roles/remove/` - Remove a user from a role
- `GET /api/users/roles/user/<user_id>/` - Get all roles assigned to a user

### Permission Management

- `GET /api/users/permissions/` - List all permissions
- `POST /api/users/permissions/assign/` - Assign a permission to a user
- `GET /api/users/permissions/check/<user_id>/<permission_codename>/` - Check if a user has a specific permission

## Usage Examples

### Creating and Assigning Roles

```python
from users.services import RoleManagementService

# Create a new role
role, created = RoleManagementService.create_role('moderator', 'Content moderator')

# Assign a user to a role
user = User.objects.get(username='john_doe')
RoleManagementService.assign_user_to_role(user, 'moderator')
```

### Checking User Roles and Permissions

```python
from users.models import User

user = User.objects.get(username='john_doe')

# Check if user has a specific role
if user.has_role('moderator'):
    # User is a moderator
    pass

# Check if user has a specific permission
if user.has_perm('users.view_user'):
    # User can view users
    pass
```

### Using Decorators in Views

```python
from users.decorators import role_required, permission_required

@role_required('admin')
@api_view(['GET'])
def admin_only_view(request):
    # Only accessible by users with 'admin' role
    pass

@permission_required('users.delete_user')
@api_view(['DELETE'])
def delete_user_view(request, user_id):
    # Only accessible by users with 'delete_user' permission
    pass
```

## Management Command

Initialize the role management system with default roles and permissions:

```bash
python manage.py init_roles
```

## Integration with Django Admin

The User admin interface has been enhanced to display user roles directly in the list view and in the user detail view.

## Extending the System

To add new roles or permissions:

1. Update the `CUSTOM_PERMISSIONS` dictionary in `users/permissions.py`
2. Update the `roles_permissions` dictionary in `users/roles.py`
3. Run the management command: `python manage.py init_roles`
