from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.roles import create_default_roles
from users.permissions import create_custom_permissions

class Command(BaseCommand):
    help = 'Initialize default roles and permissions'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating custom permissions...')
        create_custom_permissions()
        self.stdout.write(self.style.SUCCESS('Successfully created custom permissions'))  # type: ignore
        
        self.stdout.write('Creating default roles...')
        create_default_roles()
        self.stdout.write(self.style.SUCCESS('Successfully created default roles'))  # type: ignore
        
        self.stdout.write(self.style.SUCCESS('Role management system initialized successfully!'))  # type: ignore