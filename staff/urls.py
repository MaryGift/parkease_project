from django.urls import path
from . import views # This imports the functions we wrote in views.py

urlpatterns = [
   path('', views.staff_login, name='staff_login'),
   path('register/', views.register, name='register'),
]