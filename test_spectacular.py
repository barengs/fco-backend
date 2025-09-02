"""
Test file to verify drf-spectacular configuration
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('/Users/ROFI/Develop/proyek/fco_ai')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fish_chain_optimization.settings')

try:
    django.setup()
    print("Django setup successful")
    
    # Test if drf-spectacular is properly configured
    from rest_framework.settings import api_settings
    schema_class = api_settings.DEFAULT_SCHEMA_CLASS
    print(f"DEFAULT_SCHEMA_CLASS: {schema_class}")
    
    # Test if the spectacular settings are loaded
    from django.conf import settings
    if hasattr(settings, 'SPECTACULAR_SETTINGS'):
        print("SPECTACULAR_SETTINGS found")
        print(f"Title: {settings.SPECTACULAR_SETTINGS.get('TITLE', 'Not set')}")
    else:
        print("SPECTACULAR_SETTINGS not found")
        
    print("Configuration test completed successfully")
    
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()