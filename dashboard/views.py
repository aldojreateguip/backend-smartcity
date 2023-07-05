from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import folium, asyncio
from django_datatables_view.base_datatable_view import BaseDatatableView
import requests
from django.http import JsonResponse
from gps_tracking.views import tracking

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def dashboard_view(request):
    data = asyncio.run(tracking(request))
    latitud = data.get('latitude')
    longitud = data.get('longitude')
    # latitud = -3.7549937  # Obtén la latitud en tiempo real
    # longitud = -73.2673102  # Obtén la longitud en tiempo real
    
    # Crear el objeto de mapa centrado en la ubicación inicial
    mapa = folium.Map(location=[latitud, longitud], zoom_start=13, tiles='Stamen Terrain')
    
    # Agregar un marcador en la ubicación inicial
    folium.Marker([latitud, longitud], popup='Ubicación actual').add_to(mapa)
    
    # Renderizar el mapa en una plantilla HTML y devolverla como respuesta
    return render(request, 'dashboard/dashboard.html', {'mapa': mapa._repr_html_()})
   
class TuVistaDataTable(BaseDatatableView):
    def get_initial_queryset(self):
        # Aquí puedes realizar la solicitud a la API y obtener los datos
        url = 'https://demo4.traccar.org/api/positions'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return []

    def filter_queryset(self, qs):
        # Puedes implementar lógica de filtrado adicional aquí si es necesario
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            qs = [item for item in qs if search_value in item.values()]
        return qs