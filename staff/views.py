from django.shortcuts import render, redirect
from .models import Staff
from .forms import StaffForm,  StaffLoginForm
from django.contrib.auth import login as auth_login, logout

# Create your views here.
def staff_login(request):
    if request.method == 'POST':
        form = StaffLoginForm(request, data=request.POST)
        if form.is_valid():
            # Handle successful login here (e.g., authenticate and log in the user)
            userDetails = form.get_user()
            auth_login(request, userDetails)
            return redirect('dashboard')  # Redirect to a dashboard or home page after login
    else:
        form = StaffLoginForm()
    return render(request, 'staff/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the new staff member to the database
            return redirect('/')  # Redirect to login page after successful registration
    else:
        form = StaffForm()
    return render(request, 'staff/register.html', {'form': form})