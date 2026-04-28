from django.shortcuts import render, redirect, get_object_or_404
from .forms import VehicleRegistrationForm, SignOutForm
from datetime import datetime, time
from .models import Vehicle, SignOut
from tyre_clinic.models import TyreService
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def dashboard(request):
    today = timezone.now().date()
    # Count vehicles currently parked (not yet signed out)
    # We do this by checking which vehicles DO NOT have a sign-out record
    total_parked = Vehicle.objects.filter(signout__isnull=True).count()
    total_signed_out = SignOut.objects.filter(exit_time__date=today).count() # Count vehicles signed out today
    context = {
        'total_parked': total_parked,
        'total_signed_out': total_signed_out,
    }
    return render(request, 'dashboard.html', context)

def get_parking_fee(vehicle_type, arrival_time):
    hour = arrival_time.hour
    is_day = 6 <= hour < 19 # Define Day: 6am to 6:59pm (6 to 18) 
    if vehicle_type == 'TRUCK':
        return 5000 if is_day else 10000
    elif vehicle_type in ['CAR', 'TAXI']:
        return 3000 if is_day else 2000
    elif vehicle_type == 'COASTER':
        return 4000 if is_day else 2000
    elif vehicle_type == 'BODA':
        return 2000 # Same for day and night
    return 0

def register_vehicle(request):
    if request.method == "POST":
        form = VehicleRegistrationForm(request.POST)
        if form.is_valid():     
            vehicle = form.save(commit=False) # We "pause" the save so we can add the fee manually   
            now = datetime.now()
            vehicle.parking_fee = get_parking_fee(vehicle.vehicle_type, now)
            vehicle.save()     
            return redirect('vehicle_list') # After saving, let's go to a 'success' page or the list
    else:
        form = VehicleRegistrationForm() 
    return render(request, 'register.html', {'form': form})

def vehicle_list(request):
    # Only get vehicles that are currently parked
    vehicles = Vehicle.objects.filter(is_parked=True) 
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

def sign_out_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    # Get or create the sign-out record
    sign_out_instance, created = SignOut.objects.get_or_create(vehicle=vehicle)

    if request.method == "POST":
        form = SignOutForm(request.POST, instance=sign_out_instance) 
        if form.is_valid():
            sign_out = form.save(commit=False)
            sign_out.vehicle = vehicle
            sign_out.save() 
            # --- THE KEY CHANGE ---
            vehicle.is_parked = False  # Mark as gone
            vehicle.save()
            # ---------------------- 
            return redirect('vehicle_list')
    else:
        form = SignOutForm(instance=sign_out_instance)
    return render(request, 'sign_out.html', {'form': form, 'vehicle': vehicle})



@login_required
def revenue_report(request):
    # 1. PARKING REVENUE
    # This sums up every 'fee_paid' column in your SignOut table
    parking_revenue = SignOut.objects.aggregate(Sum('fee_paid'))['fee_paid__sum'] or 0
    
    # 2. TYRE CLINIC REVENUE (Example)
    tyre_revenue = TyreService.objects.aggregate(Sum('price'))['price__sum'] or 0

    # 3. GRAND TOTAL
    grand_total = parking_revenue + tyre_revenue
    
    context = {
        'parking_total': parking_revenue,
        'tyre_total': tyre_revenue,
        'grand_total': grand_total,
    }
    
    return render(request, 'revenue_report.html', context)

def sign_out_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    # Get the existing record or create a new one to prevent IntegrityError
    sign_out_instance, created = SignOut.objects.get_or_create(vehicle=vehicle)

    if request.method == "POST":
        form = SignOutForm(request.POST, instance=sign_out_instance)
        
        if form.is_valid():
            sign_out = form.save(commit=False)
            sign_out.vehicle = vehicle
            
            # --- THE MAGIC CALCULATION ---
            # This calls the method we just added to your model
            sign_out.fee_paid = sign_out.calculate_fee()
            
            sign_out.save()
            
            # Mark the vehicle as departed so it leaves the active list
            vehicle.is_parked = False
            vehicle.save()
            
            return redirect('vehicle_list')
    else:
        # For a GET request, pre-fill the form with the instance
        form = SignOutForm(instance=sign_out_instance)
        
    return render(request, 'sign_out.html', {'form': form, 'vehicle': vehicle})

def sign_out_view(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    
    if request.method == "POST":
        # 1. Capture the form data 
        name = request.POST.get('receiver_name')
        phone = request.POST.get('phone_number')
        # ... capture other fields like NIN and Gender
        
        # 2. Logic: The system must automatically calculate fees 
        # (You will write your fee logic here based on vehicle type and time)
        final_fee = 5000 # Example for a Truck during the day 

        # 3. Save the Receipt
        new_receipt = Receipt.objects.create(
            receiver_name=name,
            phone_number=phone,
            amount_paid=final_fee,
            # ... add other fields
        )
        
        # 4. Show the receipt to the user
        return render(request, 'receipt_detail.html', {'receipt': new_receipt})

    return render(request, 'sign_out.html', {'vehicle': vehicle})