from django.shortcuts import render, redirect, get_object_or_404
from .models import Battery, BatteryHire
from django.utils import timezone

# Create your views here.


def hire_battery(request):
    if request.method == "POST":
        battery_id = request.POST.get('battery')
        
        # 1. Check if battery_id actually exists in the request
        if not battery_id:
            # Handle the error or redirect back with a message
            return render(request, 'hire_form.html', {
                'error': 'Please select a battery.',
                'batteries': Battery.objects.filter(is_available=False)
            })

        # 2. Use get_object_or_404 to prevent the "DoesNotExist" crash
        battery = get_object_or_404(Battery, id=battery_id)
        
        BatteryHire.objects.create(
            battery=battery,
            customer_name=request.POST.get('customer_name'),
            customer_phone=request.POST.get('customer_phone'),
        )
        
        battery.is_available = False
        battery.save()
        return redirect('active_hires')

    available_batteries = Battery.objects.filter(is_available=True)
    return render(request, 'hire_form.html', {'batteries': available_batteries})

def return_battery(request, hire_id):
    hire = get_object_or_404(BatteryHire, id=hire_id)
    hire.return_date = timezone.now()
    hire.is_returned = True
    hire.save()
    hire.battery.is_available = True
    hire.battery.save()
    return redirect('active_hires')

def active_hires(request):
    hires = BatteryHire.objects.filter(is_returned=False)
    return render(request, 'active_hires.html', {'hires': hires})