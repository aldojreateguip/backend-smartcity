from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django_datatables_view.base_datatable_view import BaseDatatableView
import requests
import json, pytz, datetime, time
from gps_tracking.views import tracking, get_history_gps


def get_mapmarker(request):
    coordenadas = tracking(request)  # Esperar la ejecución de la función tracking
    latitud = coordenadas.get('latitude')
    longitud = coordenadas.get('longitude')
    return JsonResponse({'latitud': latitud, 'longitud': longitud})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def dashboard_view(request):
    device_url = f"{settings.TRACCAR_URL_BASE}/api/devices"
    params = {'all': True}
    
    response = requests.get(device_url, params=params, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))

    if response.status_code == 200:
        data = response.json()
        devices = []
        
        zona_horaria = pytz.timezone('America/Lima')
        
        for device in data:
            try:
                preactualizado = datetime.datetime.strptime(device.get('lastUpdate', ''), '%Y-%m-%dT%H:%M:%S.%f%z')
                fecha_hora_ajustada = preactualizado.astimezone(zona_horaria)
                actualizado = fecha_hora_ajustada.strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                actualizado = ""

            devices.append({
                'id': device.get('id', ""),
                'placa': device.get('name', ""),
                'modelo': device.get('model', "S/M"),
                'categoria': device.get('category', "S/C"),
                'actualizado': actualizado,
                'estado': device.get('status', ""),
            })

        return render(request, 'dashboard/dashboard.html', {'devices_data': devices})
    
    # Manejo de caso donde la respuesta no es 200 (opcional)
    return render(request, 'dashboard/dashboard.html', {'devices_data': []})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def devices_table(request):
    # start_time = time.time()
    # start_api_request = time.time()
    device_url = f"{settings.TRACCAR_URL_BASE}/api/devices"
    params = {'all': True}
    # print(f"Tiempo para preparar la URL y parámetros: {time.time() - start_api_request:.4f} segundos")

     # 2. Petición API
    # start_api_call = time.time()
    response = requests.get(device_url, params=params, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
    # print(f"Tiempo para llamada a la API: {time.time() - start_api_call:.4f} segundos")

    if response.status_code == 200:
        data = response.json()
        devices = []
        
        zona_horaria = pytz.timezone('America/Lima')
        
        # start_processing = time.time()

        for device in data:
            try:
                preactualizado = datetime.datetime.strptime(device.get('lastUpdate', ''), '%Y-%m-%dT%H:%M:%S.%f%z')
                fecha_hora_ajustada = preactualizado.astimezone(zona_horaria)
                actualizado = fecha_hora_ajustada.strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                actualizado = ""

            devices.append({
                'id': device.get('id', ""),
                'placa': device.get('name', ""),
                'modelo': device.get('model', "S/M"),
                'categoria': device.get('category', "S/C"),
                'actualizado': actualizado,
                'estado': device.get('status', ""),
            })
        # print(f"Tiempo para procesar los datos: {time.time() - start_processing:.4f} segundos")
        # return render(request, 'dashboard/table_devices.html', {'devices_data': devices})
        return JsonResponse({'devices_data': devices}, status = 200)
    else:
        # Manejo de caso donde la respuesta no es 200 (opcional)
        return JsonResponse({'devices_data': []}, status = 200)



def dashboard_detail(request, device_id):
    historial_response = get_history_gps(device_id)
    historial_content = historial_response.content.decode('utf-8')  # Decodificar el contenido en UTF-8
    historial_data = json.loads(historial_content)  # Cargar el contenido en un objeto JSON
    registros = historial_data["registros"]
    # return render(request, 'dashboard/table_details.html', {'dashboard_detail':registros})
    return JsonResponse({'dashboard_detail':registros})

def dashboard_detail_ajax(request, device_id):
    historial_response = get_history_gps(device_id)
    historial_content = historial_response.content.decode('utf-8')
    historial_data = json.loads(historial_content)
    registros = historial_data["registros"]
    
    # Verificar si es una solicitud AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'dashboard_detail': registros})

    return render(request, 'dashboard/dashboard_detail.html', {'dashboard_detail': registros})

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