from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import folium, asyncio
from django_datatables_view.base_datatable_view import BaseDatatableView
import requests
import threading
from gps_tracking.views import tracking


# Definir una variable global para almacenar las coordenadas
coordenadas = {}
# Función para ejecutar la captura de ubicación cada 30 segundos
async def capture_location():
    global coordenadas
    while True:
        # Ejecutar la función tracking para obtener las coordenadas
        data = await tracking(None)  # Esperar la ejecución de la función tracking
        latitud = data.get('latitude')
        longitud = data.get('longitude')

        # Actualizar las coordenadas globales
        coordenadas = {
            'latitude': latitud,
            'longitude': longitud
        }
        await asyncio.sleep(3)

# Función para iniciar el bucle principal de asyncio y el hilo de captura de ubicación
def start_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(capture_location())

# Iniciar el hilo de captura de ubicación en segundo plano
capture_thread = threading.Thread(target=start_asyncio_loop)
capture_thread.start()

def get_mapmarker(request):
    latitud = coordenadas.get('latitude')
    longitud = coordenadas.get('longitude')
    return JsonResponse({'latitud': latitud, 'longitud': longitud})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def dashboard_view(request):
    latitud = coordenadas.get('latitude')
    longitud = coordenadas.get('longitude')

    device_url = 'http://127.0.0.1:8000/devices/'
    headers = {'Authorization': settings.API_KEY_SSMC}
    data = []
    devices = requests.post(device_url, headers=headers)
    if devices.status_code == 200:
        data = devices.json()

    # Renderizar el mapa en una plantilla HTML y devolverla como respuesta
    return render(request, 'dashboard/dashboard.html', {'latitud': latitud, 'longitud': longitud, 'devices_data':data['dispositivo']})


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