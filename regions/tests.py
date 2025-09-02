from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import FishingArea

User = get_user_model()

class FishingAreaAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            user_type='ship_owner'
        )
        self.client.force_authenticate(user=self.user)
        
        self.fishing_area_data = {
            'name': 'Test Area',
            'code': 'TA001',
            'description': 'Test fishing area',
            'coordinates': '[[106.823, -6.234], [106.825, -6.232]]'
        }

    def test_create_fishing_area(self):
        """Test creating a fishing area"""
        response = self.client.post('/api/regions/create/', self.fishing_area_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(FishingArea.objects.count(), 1)  # type: ignore
        self.assertEqual(FishingArea.objects.get().name, 'Test Area')  # type: ignore

    def test_list_fishing_areas(self):
        """Test listing fishing areas"""
        FishingArea.objects.create(**self.fishing_area_data)  # type: ignore
        response = self.client.get('/api/regions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(len(response.data), 1)  # type: ignore

    def test_get_fishing_area(self):
        """Test getting a specific fishing area"""
        area = FishingArea.objects.create(**self.fishing_area_data)  # type: ignore
        response = self.client.get(f'/api/regions/{area.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(response.data['name'], 'Test Area')  # type: ignore

    def test_update_fishing_area(self):
        """Test updating a fishing area"""
        area = FishingArea.objects.create(**self.fishing_area_data)  # type: ignore
        updated_data = {
            'name': 'Updated Area',
            'code': 'TA001',
            'description': 'Updated fishing area',
            'coordinates': '[[106.823, -6.234], [106.825, -6.232]]'
        }
        response = self.client.put(f'/api/regions/{area.id}/update/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(FishingArea.objects.get().name, 'Updated Area')  # type: ignore

    def test_delete_fishing_area(self):
        """Test deleting a fishing area"""
        area = FishingArea.objects.create(**self.fishing_area_data)  # type: ignore
        response = self.client.delete(f'/api/regions/{area.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # type: ignore
        self.assertEqual(FishingArea.objects.count(), 0)  # type: ignore

    def test_download_template(self):
        """Test downloading import template"""
        response = self.client.get('/api/regions/download-template/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(response['Content-Type'], 'text/csv')  # type: ignore
        self.assertIn('attachment; filename="fishing_area_template.csv"', response['Content-Disposition'])  # type: ignore