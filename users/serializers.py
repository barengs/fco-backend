from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'ship_registration_number', 'phone_number', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'user_type': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # For ship owners and captains, ship registration number is required
        if attrs['user_type'] in ['ship_owner', 'captain'] and not attrs.get('ship_registration_number'):
            raise serializers.ValidationError("Ship registration number is required for ship owners and captains.")
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type', 'ship_registration_number', 'phone_number', 'date_joined')
        read_only_fields = ('id', 'date_joined')