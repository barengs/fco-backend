from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import csv
from .models import Ship

User = get_user_model()

class ShipModelTest(TestCase):
    def setUp(self):
        self.ship = Ship.objects.create(  # type: ignore
            name='Test Ship',
            reg_number='TS12345',
            length=20.5,
            width=5.2,
            gross_tonnage=100.5,
            year_built=2020,
            home_port='Test Port'
        )
    
    def test_ship_creation(self):
        self.assertEqual(self.ship.name, 'Test Ship')
        self.assertEqual(self.ship.reg_number, 'TS12345')
        self.assertEqual(self.ship.length, 20.5)
        self.assertEqual(self.ship.width, 5.2)
        self.assertEqual(self.ship.gross_tonnage, 100.5)
        self.assertEqual(self.ship.year_built, 2020)
        self.assertEqual(self.ship.home_port, 'Test Port')
        
    def test_ship_str_representation(self):
        expected_str = 'Test Ship (TS12345)'
        self.assertEqual(str(self.ship), expected_str)
        
    def test_ship_unique_reg_number(self):
        with self.assertRaises(Exception):
            Ship.objects.create(  # type: ignore
                name='Another Ship',
                reg_number='TS12345'  # Same reg_number
            )

class ShipAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='ship_owner'
        )
        self.ship_data = {
            'name': 'API Test Ship',
            'reg_number': 'API12345',
            'length': 25.0,
            'width': 6.5,
            'gross_tonnage': 150.0,
            'year_built': 2021,
            'home_port': 'API Test Port'
        }
        
    def test_create_ship_unauthorized(self):
        response = self.client.post('/api/ships/', self.ship_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
        
    def test_create_ship_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/ships/', self.ship_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(Ship.objects.count(), 1)  # type: ignore
        self.assertEqual(Ship.objects.get().name, 'API Test Ship')  # type: ignore
        
    def test_get_ships_unauthorized(self):
        response = self.client.get('/api/ships/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
        
    def test_get_ships_authorized(self):
        Ship.objects.create(**self.ship_data)  # type: ignore
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/ships/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(len(response.data), 1)  # type: ignore

class ShipImportTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='ship_owner'
        )
        
    def test_import_ships_csv(self):
        # Create a simple CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['name', 'reg_number', 'length', 'width', 'gross_tonnage', 'year_built', 'home_port', 'active'])
        writer.writerow(['Test Ship 1', 'TS001', '20.5', '5.2', '100.5', '2020', 'Test Port 1', 'True'])
        writer.writerow(['Test Ship 2', 'TS002', '25.0', '6.5', '150.0', '2021', 'Test Port 2', 'True'])
        
        csv_file = SimpleUploadedFile(
            "ships_test.csv",
            output.getvalue().encode('utf-8'),
            content_type="text/csv"
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/ships/import/', {'file': csv_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(Ship.objects.count(), 2)  # type: ignore
        
    def test_import_ships_csv_with_missing_required_fields(self):
        # Create a CSV file with missing required fields
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['name', 'reg_number', 'length', 'width'])
        writer.writerow(['Test Ship', '', '20.5', '5.2'])  # Missing reg_number
        writer.writerow(['', 'TS002', '25.0', '6.5'])  # Missing name
        
        csv_file = SimpleUploadedFile(
            "ships_test_invalid.csv",
            output.getvalue().encode('utf-8'),
            content_type="text/csv"
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/ships/import/', {'file': csv_file})
        self.assertEqual(response.status_code, status.HTTP_206_PARTIAL_CONTENT)  # type: ignore
        self.assertEqual(Ship.objects.count(), 0)  # type: ignore