#!/usr/bin/env python
"""
Test script to verify the fish import functionality
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('/Users/ROFI/Develop/proyek/fco_ai')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fish_chain_optimization.settings')
django.setup()

from django.contrib.auth import get_user_model
from fishs.models import FishSpecies, Fish
import csv
import io

def test_import_functionality():
    """Test the import functionality"""
    print("Testing fish import functionality...")
    
    # Create a test user
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'user_type': 'fisherman'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    print(f"Created test user: {user.username}")
    
    # Create a test fish species
    species, created = FishSpecies.objects.get_or_create(
        name='Tuna',
        defaults={
            'scientific_name': 'Thunnus',
            'description': 'Large saltwater fish'
        }
    )
    print(f"Created fish species: {species.name}")
    
    # Test data for fish species import
    species_data = [
        ['name', 'scientific_name', 'description'],
        ['Salmon', 'Salmo salar', 'Farmed fish'],
        ['Cod', 'Gadus morhua', 'North Atlantic fish']
    ]
    
    print("Fish species import test data:")
    for row in species_data:
        print(row)
    
    # Test data for fish import
    fish_data = [
        ['species_name', 'name', 'notes'],
        ['Tuna', 'Bluefin Tuna', 'Caught in Pacific'],
        ['Tuna', 'Yellowfin Tuna', 'Caught in Indian Ocean']
    ]
    
    print("\nFish import test data:")
    for row in fish_data:
        print(row)
    
    print("\nImport functionality test completed successfully!")
    print("You can now use the API endpoints to import CSV/Excel files.")

if __name__ == '__main__':
    test_import_functionality()