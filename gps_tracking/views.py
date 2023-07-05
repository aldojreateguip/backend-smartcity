from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests

@api_view(['POST'])
def obtener_ultimas_posiciones(request):
    try:
        # Obtener el token del usuario autenticado
        token = request.META.get('HTTP_AUTHORIZATION')
        # Agregar el token Bearer al encabezado Authorization
        headers = {'Authorization': f'{token}'}
        
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
        response = requests.get(url, params=params, headers=headers)
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
    except Exception as e:
        # Capturar errores no controlados y enviar un mensaje de error
        return JsonResponse({'error': str(e)})
