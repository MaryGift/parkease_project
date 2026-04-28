from django.urls import path
from . import views # This imports the functions we wrote in views.py

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_vehicle, name='register_vehicle'),
    path('list/', views.vehicle_list, name='vehicle_list'),
    path('sign-out/<int:vehicle_id>/', views.sign_out_vehicle, name='sign_out_vehicle'),
    path('reports/', views.revenue_report, name='revenue_report'),
]