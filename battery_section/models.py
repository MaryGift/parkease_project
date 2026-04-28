from django.db import models

# Create your models here.
class Battery(models.Model):
    name = models.CharField(max_length=50) # e.g., "Battery A", "Heavy Duty 1"
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class BatteryHire(models.Model):
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    hire_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    
    # Fixed pricing for the section
    deposit = models.PositiveIntegerField(default=10000)
    hire_fee = models.PositiveIntegerField(default=15000)  
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.battery.name}"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    