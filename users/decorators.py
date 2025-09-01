from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from rest_framework.response import Response
from rest_framework import status

def role_required(roles):
    """
    Decorator for views that checks whether a user has a specific role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Convert single role to list
            if isinstance(roles, str):
                roles_list = [roles]
            else:
                roles_list = roles
            
            # Check if user has any of the required roles
            user_roles = request.user.role_names
            if any(role in user_roles for role in roles_list):
                return view_func(request, *args, **kwargs)
            else:
                return Response(
                    {'error': 'Insufficient permissions'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        return _wrapped_view
    return decorator

def permission_required(permission):
    """
    Decorator for views that checks whether a user has a specific permission.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if request.user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            else:
                return Response(
                    {'error': 'Insufficient permissions'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        return _wrapped_view
    return decorator

def role_or_permission_required(roles=None, permissions=None):
    """
    Decorator for views that checks whether a user has a specific role or permission.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Check roles
            if roles:
                # Convert single role to list
                if isinstance(roles, str):
                    roles_list = [roles]
                else:
                    roles_list = roles
                
                # Check if user has any of the required roles
                user_roles = request.user.role_names
                if any(role in user_roles for role in roles_list):
                    return view_func(request, *args, **kwargs)
            
            # Check permissions
            if permissions:
                # Convert single permission to list
                if isinstance(permissions, str):
                    permissions_list = [permissions]
                else:
                    permissions_list = permissions
                
                # Check if user has any of the required permissions
                if any(request.user.has_perm(perm) for perm in permissions_list):
                    return view_func(request, *args, **kwargs)
            
            # If neither roles nor permissions match
            return Response(
                {'error': 'Insufficient permissions'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return _wrapped_view
    return decorator