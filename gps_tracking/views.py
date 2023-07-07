from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
import requests, json
import websockets
from django.conf import settings
import urllib.parse

@api_view(['POST'])
def get_devices(request):
    try:
        # Obtener el token del usuario autenticado
        token = request.META.get('HTTP_AUTHORIZATION')

        if(token == settings.API_KEY_SSMC):
            url = 'https://demo4.traccar.org/api/devices'
            
            # Realizar la solicitud GET a la API de Traccar con los parámetros
            params = {
                'all': True,
            }
            # response = requests.get(url, params=params, headers=headers)
            response = requests.get(url, params=params, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
            if response.status_code == 200:
                # Procesar la respuesta de la API de Traccar
                devices_data = response.json()
                
                # Obtener las posiciones de la respuesta y almacenarlas en la lista "posiciones"
                devices = []
                for device in devices_data:
                    id = device.get('id')
                    placa = device.get('name')
                    modelo = device.get('model')
                    categoria = device.get('category')
                    actualizado = device.get('lastUpdate')
                    estado = device.get('status')

                    devices.append({
                        'id': id, 
                        'placa': placa,
                        'modelo': modelo, 
                        'caterogia': categoria,
                        "actualizado": actualizado,
                        'estado': estado
                    })
                
                # Resto del código...
                return JsonResponse({'dispositivo': devices})
            else:
                return JsonResponse({'error': 'Error al obtener las posiciones de Traccar'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No está autorizado para acceder a esta información'}, status=401)
    except Exception as e:
        # Capturar errores no controlados y enviar un mensaje de error
        return JsonResponse({'error': str(e)})

#captura de la ultima ubicacion del gps
async def tracking(request):
    # Realizar la solicitud GET
    url = 'http://demo4.traccar.org/api/session'
    
    queryParams = {
        'token': 'RzBFAiBV2antr--FQW-jTv0Q1Vo9F2zA89oRJI9B764qzNanfAIhAIV4Mi0ifZPwGDSxgx4YAIVsrWyL6fCFHsbpZ42lEZpJeyJ1IjoxNzY0OCwiZSI6IjIwMjMtMTItMzFUMDU6MDA6MDAuMDAwKzAwOjAwIn0'
    }
    
    encodedParams = urllib.parse.urlencode(queryParams)
    
    url = f'{url}?{encodedParams}'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        cookies = response.headers.get('Set-Cookie', '')
        ws_url = 'ws://104.237.9.196:8082/api/socket'
        ws_header = {'Cookie': cookies}

        async with websockets.connect(ws_url, extra_headers=ws_header) as websocket:
            await websocket.send('Message From Client')

            while True:
                message = await websocket.recv()
                data = json.loads(message)

                positions = data.get('positions', [])
                if positions:
                    position = positions[0]
                    latitude = position.get('latitude')
                    longitude = position.get('longitude')
                    
                    coordenadas = {
                        'latitude': latitude,
                        'longitude': longitude
                    }
                    return coordenadas

    else:
        return {'status': 'error'}