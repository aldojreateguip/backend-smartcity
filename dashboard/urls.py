from django.urls import path
from . import views
from .views import TuVistaDataTable

urlpatterns = [
    #Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/<int:device_id>/', views.dashboard_detail, name='dashboard_detail'),
    path('datatable/', TuVistaDataTable.as_view(), name='datatable'),
    path('getmarker/', views.get_mapmarker, name='marker'),

]