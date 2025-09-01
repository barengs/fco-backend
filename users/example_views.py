from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .decorators import role_required, permission_required, role_or_permission_required
from .services import RoleManagementService

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required('admin')
def admin_dashboard(request):
    """
    Example view accessible only to users with 'admin' role
    """
    return Response({
        'message': 'Welcome to the admin dashboard',
        'user': request.user.username,
        'roles': request.user.role_names
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required('users.view_user')
def view_user_data(request):
    """
    Example view accessible only to users with 'view_user' permission
    """
    return Response({
        'message': 'User data view',
        'user': request.user.username,
        'has_permission': True
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_or_permission_required(roles=['admin'], permissions=['users.change_user'])
def edit_user_data(request):
    """
    Example view accessible to users with 'admin' role OR 'change_user' permission
    """
    return Response({
        'message': 'User data edit view',
        'user': request.user.username,
        'access_method': 'role_or_permission'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_role_example(request):
    """
    Example of assigning a role to a user
    """
    user_id = request.data.get('user_id')
    role_name = request.data.get('role_name')
    
    if not user_id or not role_name:
        return Response(
            {'error': 'user_id and role_name are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from .models import User
        user = User.objects.get(id=user_id)
        success = RoleManagementService.assign_user_to_role(user, role_name)
        
        if success:
            return Response({
                'message': f'Role {role_name} assigned to user {user.username}',
                'user_roles': user.role_names
            })
        else:
            return Response(
                {'error': 'Failed to assign role'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )