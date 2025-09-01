from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from .services import RoleManagementService
from .role_serializers import (
    GroupSerializer, 
    PermissionSerializer, 
    UserRoleAssignmentSerializer,
    RoleCreationSerializer,
    UserGroupSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_roles(request):
    """
    List all roles (groups) in the system
    """
    roles = Group.objects.all()
    serializer = GroupSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_role(request):
    """
    Create a new role
    """
    serializer = RoleCreationSerializer(data=request.data)
    if serializer.is_valid():
        # Handle type checking for validated_data
        validated_data = serializer.validated_data
        if validated_data and isinstance(validated_data, dict):
            role_name = validated_data.get('name', '')
            permissions = validated_data.get('permissions', [])
        else:
            return Response(
                {'error': 'Invalid data'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        group, created = RoleManagementService.create_role(role_name, permissions=permissions)
        
        if created:
            return Response(
                {'message': 'Role created successfully', 'role': GroupSerializer(group).data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Role already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_role(request, role_name):
    """
    Delete a role
    """
    success = RoleManagementService.delete_role(role_name)
    if success:
        return Response(
            {'message': 'Role deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(
            {'error': 'Role not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_permissions(request):
    """
    List all permissions in the system
    """
    permissions = Permission.objects.all()
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_user_to_role(request):
    """
    Assign a user to a role
    """
    serializer = UserRoleAssignmentSerializer(data=request.data)
    if serializer.is_valid():
        # Handle type checking for validated_data
        validated_data = serializer.validated_data
        if validated_data and isinstance(validated_data, dict):
            user_id = validated_data.get('user_id')
            role_name = validated_data.get('role_name')
        else:
            return Response(
                {'error': 'Invalid data'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            success = RoleManagementService.assign_user_to_role(user, role_name)
            
            if success:
                return Response(
                    {'message': 'User assigned to role successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Failed to assign user to role'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_user_from_role(request):
    """
    Remove a user from a role
    """
    serializer = UserRoleAssignmentSerializer(data=request.data)
    if serializer.is_valid():
        # Handle type checking for validated_data
        validated_data = serializer.validated_data
        if validated_data and isinstance(validated_data, dict):
            user_id = validated_data.get('user_id')
            role_name = validated_data.get('role_name')
        else:
            return Response(
                {'error': 'Invalid data'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            success = RoleManagementService.remove_user_from_role(user, role_name)
            
            if success:
                return Response(
                    {'message': 'User removed from role successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Failed to remove user from role'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_roles(request, user_id):
    """
    Get all roles assigned to a user
    """
    try:
        user = User.objects.get(id=user_id)
        roles = RoleManagementService.get_user_roles(user)
        serializer = GroupSerializer(roles, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_permission_to_user(request):
    """
    Assign a specific permission directly to a user
    """
    user_id = request.data.get('user_id')
    permission_codename = request.data.get('permission_codename')
    
    if not user_id or not permission_codename:
        return Response(
            {'error': 'user_id and permission_codename are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
        success = RoleManagementService.assign_permission_to_user(user, permission_codename)
        
        if success:
            return Response(
                {'message': 'Permission assigned to user successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Failed to assign permission to user'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except ObjectDoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def user_has_permission(request, user_id, permission_codename):
    """
    Check if a user has a specific permission
    """
    try:
        user = User.objects.get(id=user_id)
        has_perm = RoleManagementService.user_has_permission(user, permission_codename)
        return Response({'has_permission': has_perm})
    except ObjectDoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )