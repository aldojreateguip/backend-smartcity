from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
import requests, json
import websockets
from django.conf import settings
import urllib.parse

@api_view(['POST'])
def obtener_ultimas_posiciones(request):
    try:
        # Obtener el token del usuario autenticado
        token = request.META.get('HTTP_AUTHORIZATION')

        if(token == settings.API_KEY_SSMC):
            data = request.data
            device_param = data.get('deviceId')
            from_param = data.get('desde')
            to_param = data.get('hasta')
            url = 'https://demo4.traccar.org/api/positions'
            
            params = {
                'deviceId': device_param,
                'from': from_param,
                'to': to_param
            }
            # Realizar la solicitud GET a la API de Traccar con los parámetros
            # response = requests.get(url, params=params, headers=headers)
            response = requests.get(url, params=params, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
            if response.status_code == 200:
                # Procesar la respuesta de la API de Traccar
                data = response.json()
                
                # Obtener las posiciones de la respuesta y almacenarlas en la lista "posiciones"
                posiciones = []
                for posicion in data:
                    id = posicion.get('id')
                    deviceid = posicion.get('deviceId')
                    latitud = posicion.get('latitude')
                    longitud = posicion.get('longitude')
                    speed = posicion.get('speed')

                    posiciones.append({
                        'registro': id, 
                        'dispositivo': deviceid,
                        'latitud': latitud, 
                        'longitud': longitud,
                        "velocidad": speed
                    })
                
                # Resto del código...
                return JsonResponse({'posiciones': posiciones})
            else:
                return JsonResponse({'error': 'Error al obtener las posiciones de Traccar'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No está autorizado para acceder a esta información'}, status=401)
    except Exception as e:
        # Capturar errores no controlados y enviar un mensaje de error
        return JsonResponse({'error': str(e)})


# def tracking(request): 
#     # Realizar la solicitud GET
#     url = 'http://104.237.9.196:8082/api/session'
    
#     queryParams = {
#         'token': 'RzBFAiBV2antr--FQW-jTv0Q1Vo9F2zA89oRJI9B764qzNanfAIhAIV4Mi0ifZPwGDSxgx4YAIVsrWyL6fCFHsbpZ42lEZpJeyJ1IjoxNzY0OCwiZSI6IjIwMjMtMTItMzFUMDU6MDA6MDAuMDAwKzAwOjAwIn0'
#     }
    
#     encodedParams = urllib.parse.urlencode(queryParams)
    
#     url = f'{url}?{encodedParams}'

#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         # data = response.json()
#         # print(data)
        
#         # Establecer la conexión WebSocket
#         ws_url = 'ws://104.237.9.196:8082/api/socket'
#         cookies = response.headers.get('Set-Cookie', '')
#         ws_header = {'Cookie': cookies}
#         ws_connection = websocket.WebSocketApp(ws_url, header=ws_header)

#         def on_open(ws):
#             ws.send('Message From Client')

#         def on_error(ws, error):
#             print(f'WebSocket error: {error}')

#         def on_message(ws, message):
#             # print(message)
            
#             # Analizar el mensaje JSON recibido
#             data = json.loads(message)
            
#             # Obtener la lista de posiciones
#             positions = data.get('positions', [])
            
#             if positions:
#                 # Tomar la primera posición de la lista (suponiendo que solo hay una posición en el mensaje)
#                 position = positions[0]
                
#                 # Extraer los valores de latitude y longitude
#                 latitude = position.get('latitude')
#                 longitude = position.get('longitude')
                
#                 # Imprimir los valores de latitude y longitude
#                 # coordenadas = {
#                 #     'latitude': latitude,
#                 #     'longitude': longitude
#                 # }
#                 print('enviar coordenadas')
#                 # return coordenadas
#                 return {'latitude': latitude, 'longitude': longitude}


#         ws_connection.on_open = on_open
#         ws_connection.on_error = on_error
#         ws_connection.on_message = on_message

#         # Iniciar la conexión WebSocket en un subproceso separado
#         ws_connection.run_forever()

#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error'})
    

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