from django.urls import path
from . import views

urlpatterns = [
    #Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

]