from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from typing import cast
from role_permission.services import RoleManagementService

User = get_user_model()

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.ship_owner_data = {
            'username': 'testshipowner',
            'email': 'shipowner@example.com',
            'role': 'ship_owner',
            'owner_type': 'individual',
            'phone_number': '081234567890',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        
        self.captain_data = {
            'username': 'testcaptain',
            'email': 'captain@example.com',
            'role': 'captain',
            'license_number': 'CAPT001',
            'years_of_experience': 10,
            'phone_number': '081234567891',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        
        self.admin_data = {
            'username': 'testadmin',
            'email': 'admin@example.com',
            'role': 'admin',
            'employee_id': 'EMP001',
            'department': 'Operations',
            'position': 'Manager',
            'phone_number': '081234567892',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }

    def test_register_ship_owner_success(self):
        """Test successful ship owner registration"""
        response = cast(Response, self.client.post('/api/users/register/', self.ship_owner_data, format='json'))
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertIn('user', response.data)  # type: ignore
        self.assertIn('tokens', response.data)  # type: ignore
        self.assertIn('access', response.data['tokens'])  # type: ignore
        self.assertIn('refresh', response.data['tokens'])  # type: ignore
        
        # Check if user was created in database
        self.assertTrue(User.objects.filter(username='testshipowner').exists())
        
        # Check if ship owner profile was created
        user = User.objects.get(username='testshipowner')
        self.assertTrue(hasattr(user, 'ship_owner_profile'))

    def test_register_captain_success(self):
        """Test successful captain registration"""
        response = cast(Response, self.client.post('/api/users/register/', self.captain_data, format='json'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertIn('user', response.data)  # type: ignore
        self.assertIn('tokens', response.data)  # type: ignore
        self.assertIn('access', response.data['tokens'])  # type: ignore
        self.assertIn('refresh', response.data['tokens'])  # type: ignore
        
        # Check if user was created in database
        self.assertTrue(User.objects.filter(username='testcaptain').exists())
        
        # Check if captain profile was created
        user = User.objects.get(username='testcaptain')
        self.assertTrue(hasattr(user, 'captain_profile'))

    def test_register_admin_success(self):
        """Test successful admin registration"""
        response = cast(Response, self.client.post('/api/users/register/', self.admin_data, format='json'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertIn('user', response.data)  # type: ignore
        self.assertIn('tokens', response.data)  # type: ignore
        self.assertIn('access', response.data['tokens'])  # type: ignore
        self.assertIn('refresh', response.data['tokens'])  # type: ignore
        
        # Check if user was created in database
        self.assertTrue(User.objects.filter(username='testadmin').exists())
        
        # Check if admin profile was created
        user = User.objects.get(username='testadmin')
        self.assertTrue(hasattr(user, 'admin_profile'))

    def test_register_user_password_mismatch(self):
        """Test user registration with password mismatch"""
        data = self.ship_owner_data.copy()
        data['password_confirm'] = 'differentpassword'
        response = cast(Response, self.client.post('/api/users/register/', data, format='json'))
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore
        self.assertIn('non_field_errors', response.data)  # type: ignore

    def test_register_ship_owner_missing_required_fields(self):
        """Test ship owner registration with missing required fields"""
        data = self.ship_owner_data.copy()
        data['owner_type'] = 'company'
        # Missing company_name for company owner
        response = cast(Response, self.client.post('/api/users/register/', data, format='json'))
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore

    def test_register_captain_missing_required_fields(self):
        """Test captain registration with missing required fields"""
        data = self.captain_data.copy()
        data['license_number'] = ''
        response = cast(Response, self.client.post('/api/users/register/', data, format='json'))
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore

    def test_register_admin_missing_required_fields(self):
        """Test admin registration with missing required fields"""
        data = self.admin_data.copy()
        data['employee_id'] = ''
        response = cast(Response, self.client.post('/api/users/register/', data, format='json'))
        # Type ignore to fix basedpyright error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore

    def test_login_user_success(self):
        """Test successful user login"""
        # First create a user
        register_response = cast(Response, self.client.post('/api/users/register/', self.ship_owner_data, format='json'))
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)  # type: ignore
        
        # Then login with the same credentials
        login_data = {
            'username': 'testshipowner',
            'password': 'testpassword123'
        }
        response = cast(Response, self.client.post('/api/users/login/', login_data, format='json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertIn('user', response.data)  # type: ignore
        self.assertIn('tokens', response.data)  # type: ignore
        self.assertIn('access', response.data['tokens'])  # type: ignore
        self.assertIn('refresh', response.data['tokens'])  # type: ignore

    def test_login_user_invalid_credentials(self):
        """Test user login with invalid credentials"""
        login_data = {
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }
        response = cast(Response, self.client.post('/api/users/login/', login_data, format='json'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
        self.assertIn('error', response.data)  # type: ignore

    def test_token_refresh_success(self):
        """Test successful token refresh"""
        # First create and login a user
        register_response = cast(Response, self.client.post('/api/users/register/', self.ship_owner_data, format='json'))
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)  # type: ignore
        
        # Get refresh token from registration
        refresh_token = register_response.data['tokens']['refresh'] if register_response.data else ''  # type: ignore
        
        # Refresh the token
        refresh_data = {
            'refresh': refresh_token
        }
        response = cast(Response, self.client.post('/api/users/token/refresh/', refresh_data, format='json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertIn('access', response.data)  # type: ignore

    def test_logout_user_success(self):
        """Test successful user logout"""
        # First create and login a user
        register_response = cast(Response, self.client.post('/api/users/register/', self.ship_owner_data, format='json'))
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)  # type: ignore
        
        # Get refresh token
        refresh_token = register_response.data['tokens']['refresh'] if register_response.data else ''  # type: ignore
        
        # Logout with refresh token
        logout_data = {
            'refresh': refresh_token
        }
        response = cast(Response, self.client.post('/api/users/logout/', logout_data, format='json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertIn('message', response.data)  # type: ignore

    def test_get_user_profile(self):
        """Test getting user profile"""
        # First create and login a user
        register_response = cast(Response, self.client.post('/api/users/register/', self.ship_owner_data, format='json'))
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)  # type: ignore
        
        # Get access token
        access_token = register_response.data['tokens']['access'] if register_response.data else ''  # type: ignore
        
        # Authenticate client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Get user profile
        response = cast(Response, self.client.get('/api/users/profile/'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertIn('role_names', response.data)  # type: ignore
        self.assertIn('ship_owner_profile', response.data)  # type: ignore

    def test_update_ship_owner_profile(self):
        """Test updating ship owner profile"""
        # First create and login a user
        register_response = cast(Response, self.client.post('/api/users/register/', self.ship_owner_data, format='json'))
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)  # type: ignore
        
        # Get access token
        access_token = register_response.data['tokens']['access'] if register_response.data else ''  # type: ignore
        
        # Authenticate client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Update ship owner profile
        update_data = {
            'address': '123 Main St',
            'contact_person': 'John Doe'
        }
        response = cast(Response, self.client.put('/api/users/profile/ship-owner/update/', update_data, format='json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertIn('address', response.data)  # type: ignore
        self.assertEqual(response.data['address'], '123 Main St')  # type: ignore
