from django.shortcuts import render, redirect
from .forms import TyreServiceForm
from .models import TyreService, TyreOption

# Create your views here.
def record_service(request):
    if request.method == "POST":
        form = TyreServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_history')
    else:
        form = TyreServiceForm()
    return render(request, 'record_service.html', {'form': form})

def service_history(request):
    services = TyreService.objects.all().order_by('-service_date')
    return render(request, 'service_history.html', {'services': services})

def record_tyre_service(request):
    if request.method == 'POST':
        form = TyreServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print(form.errors) # This will show you in the terminal WHY it didn't save
    else:
        form = TyreServiceForm()
    
    return render(request, 'record_service.html', {'form': form})