from django.urls import path
from . import views

urlpatterns = [
    path('receive-gps-data/', views.receive_gps_data, name='receive_gps_data'),
]