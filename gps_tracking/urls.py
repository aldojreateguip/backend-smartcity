from django.urls import path
from . import views

urlpatterns = [
    path('receive-gps-data/', views.start_server_view, name='receive_gps_data'),
]