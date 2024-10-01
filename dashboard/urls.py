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
    path('gethistory/<int:device_id>/', views.dashboard_detail_ajax, name='history_details'),
    path('getdevicesdata/', views.devices_table, name='devices_data'),
    # path('datatable/', TuVistaDataTable.as_view(), name='datatable'),
    path('getmarker/', views.get_mapmarkers, name='marker'),
    path('getmarker/<int:device_id>/', views.get_mapmarker, name='markerid'),

]