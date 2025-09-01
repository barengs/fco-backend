from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ship_owner', 'Ship Owner'),
        ('captain', 'Captain'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    ship_registration_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # For ship owners and captains, we'll use either username or ship registration number for login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_type', 'email']
    
    def __str__(self):
        # Using getattr to avoid type checking issues
        display_method = getattr(self, 'get_user_type_display', None)
        if display_method:
            user_type_display = display_method()
        else:
            # Fallback to showing the raw value
            user_type_display = self.user_type
        return f"{self.username} ({user_type_display})"
    
    def is_ship_owner(self):
        return self.user_type == 'ship_owner'
        
    def is_captain(self):
        return self.user_type == 'captain'
        
    def is_admin(self):
        return self.user_type == 'admin'