from django.urls import path
from . import views
from .views import TuVistaDataTable
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    #Dashboard
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/<int:device_id>/', views.dashboard_detail, name='dashboard_detail'),
    path('datatable/', TuVistaDataTable.as_view(), name='datatable'),
    path('getmarker/', views.get_mapmarker, name='marker'),

]