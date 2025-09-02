from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import csv
from .models import FishSpecies, Fish

User = get_user_model()

class FishSpeciesModelTest(TestCase):
    def setUp(self):
        self.fish_species = FishSpecies.objects.create(  # type: ignore
            name='Tuna',
            scientific_name='Thunnus',
            description='Large saltwater fish'
        )
    
    def test_fish_species_creation(self):
        self.assertEqual(self.fish_species.name, 'Tuna')
        self.assertEqual(self.fish_species.scientific_name, 'Thunnus')
        self.assertEqual(self.fish_species.description, 'Large saltwater fish')
        
    def test_fish_species_str_representation(self):
        self.assertEqual(str(self.fish_species), 'Tuna')
        
    def test_fish_species_unique_name(self):
        with self.assertRaises(Exception):
            FishSpecies.objects.create(name='Tuna')  # Same name  # type: ignore

class FishModelTest(TestCase):
    def setUp(self):
        self.species = FishSpecies.objects.create(  # type: ignore
            name='Salmon',
            scientific_name='Salmo salar'
        )
        self.fish = Fish.objects.create(  # type: ignore
            species=self.species,
            name='Atlantic Salmon',
            notes='Caught in Norwegian waters'
        )
    
    def test_fish_creation(self):
        self.assertEqual(self.fish.name, 'Atlantic Salmon')
        self.assertEqual(self.fish.species, self.species)
        self.assertEqual(self.fish.notes, 'Caught in Norwegian waters')
        
    def test_fish_str_representation(self):
        expected_str = 'Atlantic Salmon (Salmon)'
        self.assertEqual(str(self.fish), expected_str)
        
    def test_fish_without_name(self):
        fish_without_name = Fish.objects.create(  # type: ignore
            species=self.species,
            notes='No name provided'
        )
        expected_str = 'Ikan Salmon'
        self.assertEqual(str(fish_without_name), expected_str)

class FishSpeciesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='fisherman'
        )
        self.species_data = {
            'name': 'Cod',
            'scientific_name': 'Gadus morhua',
            'description': 'Common North Atlantic fish'
        }
        
    def test_create_species_unauthorized(self):
        response = self.client.post('/api/fishs/species/', self.species_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
        
    def test_create_species_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/fishs/species/', self.species_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(FishSpecies.objects.count(), 1)  # type: ignore
        self.assertEqual(FishSpecies.objects.get().name, 'Cod')  # type: ignore
        
    def test_get_species_unauthorized(self):
        response = self.client.get('/api/fishs/species/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
        
    def test_get_species_authorized(self):
        FishSpecies.objects.create(**self.species_data)  # type: ignore
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/fishs/species/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(len(response.data), 1)  # type: ignore

class FishAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='fisherman'
        )
        self.species = FishSpecies.objects.create(  # type: ignore
            name='Mackerel',
            scientific_name='Scomber scombrus'
        )
        self.fish_data = {
            'species': self.species.id,
            'name': 'Spanish Mackerel',
            'notes': 'Caught in Mediterranean'
        }
        
    def test_create_fish_unauthorized(self):
        response = self.client.post('/api/fishs/fish/', self.fish_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
        
    def test_create_fish_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/fishs/fish/', self.fish_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(Fish.objects.count(), 1)  # type: ignore
        self.assertEqual(Fish.objects.get().name, 'Spanish Mackerel')  # type: ignore
        
    def test_get_fish_unauthorized(self):
        response = self.client.get('/api/fishs/fish/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
        
    def test_get_fish_authorized(self):
        Fish.objects.create(  # type: ignore
            species=self.species,
            name='Spanish Mackerel',
            notes='Caught in Mediterranean'
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/fishs/fish/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(len(response.data), 1)  # type: ignore

class FishImportTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='fisherman'
        )
        self.species = FishSpecies.objects.create(  # type: ignore
            name='Tuna',
            scientific_name='Thunnus'
        )
        
    def test_import_fish_species_csv(self):
        # Create a simple CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['name', 'scientific_name', 'description'])
        writer.writerow(['Salmon', 'Salmo salar', 'Farmed fish'])
        writer.writerow(['Cod', 'Gadus morhua', 'North Atlantic fish'])
        
        csv_file = SimpleUploadedFile(
            "species_test.csv",
            output.getvalue().encode('utf-8'),
            content_type="text/csv"
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/fishs/species/import/', {'file': csv_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(FishSpecies.objects.count(), 3)  # type: ignore
        
    def test_import_fish_csv(self):
        # Create a simple CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['species_name', 'name', 'notes'])
        writer.writerow(['Tuna', 'Bluefin Tuna', 'Caught in Pacific'])
        writer.writerow(['Tuna', 'Yellowfin Tuna', 'Caught in Indian Ocean'])
        
        csv_file = SimpleUploadedFile(
            "fish_test.csv",
            output.getvalue().encode('utf-8'),
            content_type="text/csv"
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/fishs/fish/import/', {'file': csv_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(Fish.objects.count(), 2)  # type: ignore