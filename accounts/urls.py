from django.urls import path
from . import views

urlpatterns = [
    #Login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #Register by Steps
    path('register/', views.register_view, name='register'),
    path('register/step2/', views.register_step2_view, name='register_step2'),

]