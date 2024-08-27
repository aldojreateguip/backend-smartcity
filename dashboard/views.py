from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django_datatables_view.base_datatable_view import BaseDatatableView
import requests
import json
from gps_tracking.views import tracking, get_history_gps


def get_mapmarker(request):
    coordenadas = tracking(request)  # Esperar la ejecución de la función tracking
    latitud = coordenadas.get('latitude')
    longitud = coordenadas.get('longitude')
    return JsonResponse({'latitud': latitud, 'longitud': longitud})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def dashboard_view(request):
    coordenadas = tracking(request)  # Esperar la ejecución de la función tracking
    latitud = coordenadas.get('latitude')
    longitud = coordenadas.get('longitude')

    device_url = settings.API_URL_BASE + '/devices/'
    headers = {'Authorization': settings.API_KEY_SSMC}
    data = []
    print('solicitando datos de dispositivos')
    devices = requests.post(device_url, headers=headers)
    print('dispositivos obtenidos')
    print(devices)
    if devices.status_code == 200:
        data = devices.json()

    print(data)
    # Renderizar el mapa en una plantilla HTML y devolverla como respuesta
    return render(request, 'dashboard/dashboard.html', {'latitud': latitud, 'longitud': longitud, 'devices_data':data['dispositivo']})


def dashboard_detail(request, device_id):
    historial_response = get_history_gps(device_id)
    historial_content = historial_response.content.decode('utf-8')  # Decodificar el contenido en UTF-8
    historial_data = json.loads(historial_content)  # Cargar el contenido en un objeto JSON
    registros = historial_data["registros"]
    return render(request, 'dashboard/dashboard_detail.html', {'dashboard_detail':registros})


class TuVistaDataTable(BaseDatatableView):
    def get_initial_queryset(self):
        url = settings.TRACCAR_URL_BASE + '/api/positions'
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