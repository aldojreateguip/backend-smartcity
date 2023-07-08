from django.urls import path
from gps_tracking import views


urlpatterns = [
    path('devices/', views.get_devices, name='devices'),
    path('history/', views.get_history_gps, name='history'),
]