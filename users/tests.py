from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        
        # Check if user was created in database
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_password_mismatch(self):
        """Test user registration with password mismatch"""
        data = self.user_data.copy()
        data['password_confirm'] = 'differentpassword'
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_register_user_missing_ship_registration(self):
        """Test user registration for ship owner without ship registration number"""
        data = self.user_data.copy()
        data['ship_registration_number'] = ''
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)