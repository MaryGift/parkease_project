from django.urls import path
from . import views

urlpatterns = [
    path('hire/', views.hire_battery, name='hire_battery'),
    path('active/', views.active_hires, name='active_hires'),
    path('return/<int:hire_id>/', views.return_battery, name='return_battery'),
]