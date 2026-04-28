from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Staff(AbstractUser):
    ROLES = [('ADMIN', 'admin'), ('ATTENDANT', 'attendant')]
    roles = models.CharField(max_length=50, choices=ROLES)
    
    def __str__(self):
        return self.username
    # You can add additional fields here if needed
    pass