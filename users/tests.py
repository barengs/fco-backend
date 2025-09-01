from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient
from rest_framework import status
from .services import RoleManagementService

User = get_user_model()

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'user_type': 'ship_owner',
            'ship_registration_number': 'SRN123456',
            'phone_number': '081234567890',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }

    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post('/api/users/register/', self.user_data, format='json')
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertIn('user', response.data)  # type: ignore
        self.assertIn('token', response.data)  # type: ignore
        
        # Check if user was created in database
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_password_mismatch(self):
        """Test user registration with password mismatch"""
        data = self.user_data.copy()
        data['password_confirm'] = 'differentpassword'
        response = self.client.post('/api/users/register/', data, format='json')
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore
        self.assertIn('non_field_errors', response.data)  # type: ignore

    def test_register_user_missing_ship_registration(self):
        """Test user registration for ship owner without ship registration number"""
        data = self.user_data.copy()
        data['ship_registration_number'] = ''
        response = self.client.post('/api/users/register/', data, format='json')
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore


class RoleManagementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='ship_owner'
        )
        
    def test_create_role(self):
        """Test creating a new role"""
        role, created = RoleManagementService.create_role('test_role')
        self.assertTrue(created)
        self.assertIsInstance(role, Group)
        self.assertEqual(role.name, 'test_role')
        
    def test_assign_user_to_role(self):
        """Test assigning a user to a role"""
        # Create a role first
        RoleManagementService.create_role('test_role')
        
        # Assign user to role
        result = RoleManagementService.assign_user_to_role(self.user, 'test_role')
        self.assertTrue(result)
        
        # Check if user has the role
        self.assertTrue(self.user.has_role('test_role'))
        
    def test_user_role_property(self):
        """Test user role properties"""
        # Create and assign roles
        RoleManagementService.create_role('role1')
        RoleManagementService.create_role('role2')
        RoleManagementService.assign_user_to_role(self.user, 'role1')
        RoleManagementService.assign_user_to_role(self.user, 'role2')
        
        # Check role names property
        role_names = self.user.role_names
        self.assertIn('role1', role_names)
        self.assertIn('role2', role_names)
        
    def test_remove_user_from_role(self):
        """Test removing a user from a role"""
        # Create and assign role
        RoleManagementService.create_role('test_role')
        RoleManagementService.assign_user_to_role(self.user, 'test_role')
        
        # Remove user from role
        result = RoleManagementService.remove_user_from_role(self.user, 'test_role')
        self.assertTrue(result)
        
        # Check if user no longer has the role
        self.assertFalse(self.user.has_role('test_role'))