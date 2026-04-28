from django.db import models
import uuid # This is for generating unique receipt numbers
from django.utils import timezone
from datetime import time

class Vehicle(models.Model): 
    VEHICLE_CHOICES = [
        ('TRUCK', 'Truck'),
        ('CAR', 'Personal Car'),
        ('TAXI', 'Taxi'),
        ('COASTER', 'Coaster'),
        ('BODA', 'Boda-boda'),
    ]

    driver_name = models.CharField(max_length=100) 
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    number_plate = models.CharField(max_length=10) 
    vehicle_model = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15) 
    nin_number = models.CharField(max_length=20, blank=True, null=True) 
    arrival_time = models.DateTimeField(auto_now_add=True)
    is_parked = models.BooleanField(default=True)

    def __str__(self):
        return self.number_plate

class SignOut(models.Model):
    # 1. Connect this to the specific vehicle
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    
    # 2. Add the fields your SignOutForm will capture
    receiver_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    nin_number = models.CharField(max_length=14)
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # 3. Time and Money
    exit_time = models.DateTimeField(auto_now_add=True)
    fee_paid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Automatically generate a receipt number before saving
        if not self.receipt_number:
            self.receipt_number = "REC-" + str(uuid.uuid4().hex[:6]).upper()
        super().save(*args, **kwargs)

    def calculate_fee(self):
        entry_time = self.vehicle.arrival_time
        current_exit_time = timezone.now()
        
        duration = current_exit_time - entry_time
        duration_hours = duration.total_seconds() / 3600
        
        day_start = time(6, 0)
        night_start = time(19, 0)
        entry_hour = entry_time.time()
        is_daytime = day_start <= entry_hour < night_start

        rates = {
            'TRUCK': (2000, 5000, 10000),   
            'CAR': (2000, 3000, 2000),
            'TAXI': (2000, 3000, 2000),
            'COASTER': (3000, 4000, 2000),
            'BODA': (1000, 2000, 2000),
        }

        short_rate, day_rate, night_rate = rates.get(self.vehicle.vehicle_type, (2000, 2000, 2000))

        if duration_hours < 3:
            return short_rate
        elif is_daytime:
            return day_rate
        else:
            return night_rate

    def __str__(self):
        return f"Sign-out for {self.vehicle.number_plate}"