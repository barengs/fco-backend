from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from .models import User

class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permission model
    """
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'content_type')
        read_only_fields = ('id', 'name', 'codename', 'content_type')

class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Group (Role) model
    """
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')
        read_only_fields = ('id', 'permissions')

class UserGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for assigning users to groups
    """
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = ('id', 'username', 'groups')
        
    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        if groups is not None:
            instance.groups.set(groups)
        return instance

class UserRoleAssignmentSerializer(serializers.Serializer):
    """
    Serializer for assigning roles to users
    """
    user_id = serializers.IntegerField()
    role_name = serializers.CharField(max_length=150)
    
    def validate_user_id(self, value):
        try:
            User.objects.get(id=value)
            return value
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User does not exist.")
    
    def validate_role_name(self, value):
        try:
            Group.objects.get(name=value)
            return value
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Role does not exist.")

class RoleCreationSerializer(serializers.Serializer):
    """
    Serializer for creating new roles
    """
    name = serializers.CharField(max_length=150)
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
    
    def validate_name(self, value):
        if Group.objects.filter(name=value).exists():
            raise serializers.ValidationError("Role with this name already exists.")
        return value