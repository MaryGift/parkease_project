from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record_service, name='record_service'),
    path('history/', views.service_history, name='service_history'),
]