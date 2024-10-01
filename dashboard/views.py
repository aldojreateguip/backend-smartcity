from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django_datatables_view.base_datatable_view import BaseDatatableView
import requests
import json, pytz, datetime, time, urllib.parse
from gps_tracking.views import tracking, get_history_gps
from django.views.decorators.csrf import csrf_exempt


def get_mapmarker(request, device_id):
    api_url = settings.TRACCAR_URL_BASE + '/api/postitions'
    fecha_actual = datetime.datetime.now()

    queryParams = {
        'deviceId': device_id,
        'from':fecha_actual,
        'to': fecha_actual
    }
    
    encodedParams = urllib.parse.urlencode(queryParams)
    
    url = f'{api_url}?{encodedParams}'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        coordenadas = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
        }
        return coordenadas
    latitud = coordenadas.get('latitude')
    longitud = coordenadas.get('longitude')
    return JsonResponse({'latitud': latitud, 'longitud': longitud})

def get_mapmarkers(request):
    headers = {
        'Content-Type': 'application/json'
    }

    # Obtiene los devices
    devices_api = settings.TRACCAR_URL_BASE + '/api/devices'
    deviceData = {
        'all': 'true',
        'userid': '4184'
    }
    devicesResponse = requests.get(devices_api, params=deviceData, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
    
    coordenadas_devices = {}
    devicesId = []
    if devicesResponse.status_code == 200:
        devices = devicesResponse.json()
        for device in devices:
            devicesId.append(device['id'])

        for device_id in devicesId:
            # Para cada dispositivo, obtener la última posición
            position_api = settings.TRACCAR_URL_BASE + '/api/positions'
            fecha_actual = datetime.datetime.now().isoformat() + 'Z' # Fecha actual en formato ISO

            positionData = {
                'deviceId': device_id,
                'to': fecha_actual  # Obtendremos la posición más reciente hasta ahora
            }
            positionEncodedParams = urllib.parse.urlencode(positionData)
            position_url = f'{position_api}?{positionEncodedParams}'
            # print(position_url)
            positionResponse = requests.get(position_url, headers=headers, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
            # print(positionResponse)
            if positionResponse.status_code == 200:
                positions = positionResponse.json()
                
                if positions:
                    # Obtén la última posición (suponiendo que esté en la primera posición del array)
                    last_position = positions[0] if isinstance(positions, list) else positions

                    coordenadas = {
                        "latitude": last_position.get("latitude"),
                        "longitude": last_position.get("longitude"),
                    }
                    coordenadas_devices[device_id] = coordenadas
                else:
                    # Si no hay posiciones para ese device
                    coordenadas_devices[device_id] = {"message": "No hay posiciones disponibles"}
    return JsonResponse({'coordenadas': coordenadas_devices})

@csrf_exempt
def get_mapmarkers2(request):
    headers = {
        'Content-Type': 'application/json'
    }

    # Obtiene los devices
    devices_api = settings.TRACCAR_URL_BASE + '/api/devices'
    deviceData = {
        'all': 'true',
        'userid': '4184'
    }
    devicesResponse = requests.get(devices_api, params=deviceData, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
    
    coordenadas_devices = {}
    devicesId = []
    if devicesResponse.status_code == 200:
        devices = devicesResponse.json()
        for device in devices:
            devicesId.append(device['id'])

        for device_id in devicesId:
            # Para cada dispositivo, obtener la última posición
            position_api = settings.TRACCAR_URL_BASE + '/api/positions'
            fecha_actual = datetime.datetime.now().isoformat() + 'Z' # Fecha actual en formato ISO

            positionData = {
                'deviceId': device_id,
                'to': fecha_actual  # Obtendremos la posición más reciente hasta ahora
            }
            positionEncodedParams = urllib.parse.urlencode(positionData)
            position_url = f'{position_api}?{positionEncodedParams}'
            # print(position_url)
            positionResponse = requests.get(position_url, headers=headers, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
            # print(positionResponse)
            if positionResponse.status_code == 200:
                positions = positionResponse.json()
                
                if positions:
                    # Obtén la última posición (suponiendo que esté en la primera posición del array)
                    last_position = positions[0] if isinstance(positions, list) else positions

                    coordenadas = {
                        "latitude": last_position.get("latitude"),
                        "longitude": last_position.get("longitude"),
                    }
                    coordenadas_devices[device_id] = coordenadas
                else:
                    # Si no hay posiciones para ese device
                    coordenadas_devices[device_id] = {"message": "No hay posiciones disponibles"}
    return coordenadas_devices

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html', status=200)


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
    coords_markers = get_mapmarkers2(request)
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
        return JsonResponse({'devices_data': devices, 'coords_marker': coords_markers}, status = 200)
    else:
        # Manejo de caso donde la respuesta no es 200 (opcional)
        return JsonResponse({'devices_data': []}, status = 200)



def dashboard_detail(request, device_id):
    historial_response = get_history_gps(device_id)
    historial_content = historial_response.content.decode('utf-8')  # Decodificar el contenido en UTF-8
    historial_data = json.loads(historial_content) # Cargar el contenido en un objeto JSON
    # Recorrer y eliminar los campos 'motion' y 'evento'
    
    registros = historial_data["registros"]
    lat_marker = registros[len(registros)-1]['latitud']
    lon_marker = registros[len(registros)-1]['longitud']
    # return render(request, 'dashboard/table_details.html', {'dashboard_detail':registros})
    return JsonResponse({'dashboard_detail':registros,'lat_marker':lat_marker,'lon_marker':lon_marker})

def dashboard_detail_ajax(request, device_id):
    historial_response = get_history_gps(device_id)
    historial_content = historial_response.content.decode('utf-8')
    historial_data = json.loads(historial_content)
    registros = historial_data["registros"]
    
    # print(registros)
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