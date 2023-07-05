from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.backends import BaseBackend
from django.http import JsonResponse
import folium

def dashboard_view(request):
    latitud = 37.7749  # Obtén la latitud en tiempo real
    longitud = -122.4194  # Obtén la longitud en tiempo real
    
    # Crear el objeto de mapa centrado en la ubicación inicial
    mapa = folium.Map(location=[latitud, longitud], zoom_start=13, tiles='Stamen Terrain')
    
    # Agregar un marcador en la ubicación inicial
    folium.Marker([latitud, longitud], popup='Ubicación actual').add_to(mapa)
    
    # Renderizar el mapa en una plantilla HTML y devolverla como respuesta
    return render(request, 'dashboard/dashboard.html', {'mapa': mapa._repr_html_()})


def mapa(request):
    latitud = 37.7749  # Obtén la latitud en tiempo real
    longitud = -122.4194  # Obtén la longitud en tiempo real
    
    # Crear el objeto de mapa centrado en la ubicación inicial
    mapa = folium.Map(location=[latitud, longitud], zoom_start=13)
    
    # Agregar un marcador en la ubicación inicial
    folium.Marker([latitud, longitud], popup='Ubicación actual').add_to(mapa)
    
    # Renderizar el mapa en una plantilla HTML y devolverla como respuesta
    return render(request, 'dashboard/dashboard.html', {'mapa': mapa._repr_html_()})