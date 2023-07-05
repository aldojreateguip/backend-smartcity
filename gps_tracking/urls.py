from django.urls import path
from gps_tracking import views


urlpatterns = [
    path('position/latest', views.obtener_ultimas_posiciones, name='get_position'),
    path('tracking', views.tracking, name='on_tracking')


]