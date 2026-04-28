from django.db import models
from parking_system.models import Vehicle # We link to the existing Vehicle records

# Create your models here.
class TyreService(models.Model):
    SERVICE_CHOICES = [
        ('pressure', 'Pressure (UGX 500)'),
        ('puncture', 'Puncture Fixing (UGX 5,000)'),
        ('valves', 'Valves (UGX 5,000)'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    service_date = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField() # Price can be set by the manager
    attendant_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.vehicle.number_plate} - {self.service_type}"
    
from django.db import models

class TyreOption(models.Model):
    # This stores the name (e.g., "Puncture Fixing") and the price (e.g., 5000)
    service_name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        # This makes the name show up nicely in the Admin panel
        return f"{self.service_name} - UGX {self.price}"