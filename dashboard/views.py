from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django_datatables_view.base_datatable_view import BaseDatatableView
import requests
from gps_tracking.views import tracking
from rest_framework.decorators import api_view


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
    devices = requests.post(device_url, headers=headers)
    if devices.status_code == 200:
        data = devices.json()

    # Renderizar el mapa en una plantilla HTML y devolverla como respuesta
    return render(request, 'dashboard/dashboard.html', {'latitud': latitud, 'longitud': longitud, 'devices_data':data['dispositivo']})


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