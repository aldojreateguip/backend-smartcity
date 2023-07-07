from django.urls import path
from gps_tracking import views


urlpatterns = [
    path('devices/', views.get_devices, name='get_position'),
    path('tracking', views.tracking, name='on_tracking')


]