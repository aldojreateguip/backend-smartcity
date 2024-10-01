from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
import requests, json
import websockets
from django.conf import settings
import urllib.parse
import datetime
import pytz
from geopy.distance import geodesic


@api_view(['POST'])
def get_devices(request):
    try:
        # Obtener el token del usuario autenticado
        token = request.META.get('HTTP_AUTHORIZATION')

        if token == settings.API_KEY_SSMC:
            url = settings.TRACCAR_URL_BASE + '/api/devices'
            
            # Realizar la solicitud GET a la API de Traccar con los parámetros
            params = {
                'all': True,
            }
            response = requests.get(url, params=params, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))
            if response.status_code == 200:
                # Procesar la respuesta de la API de Traccar
                devices_data = response.json()
                
                # Obtener las posiciones de la respuesta y almacenarlas en la lista "devices"
                devices = []
                for device in devices_data:
                    id = device.get('id', "")
                    placa = device.get('name', "")
                    modelo = device.get('model', "")
                    categoria = device.get('category', "")
                    fecha_hora_utc = device.get('lastUpdate', "")
                    estado = device.get('status', "")
                    
                    if isinstance(fecha_hora_utc, str) and fecha_hora_utc:
                        try:
                            preactualizado = datetime.datetime.strptime(fecha_hora_utc, '%Y-%m-%dT%H:%M:%S.%f%z')
                            zona_horaria = pytz.timezone('America/Lima')
                            fecha_hora_ajustada = preactualizado.astimezone(zona_horaria)
                            actualizado = fecha_hora_ajustada.strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            actualizado = ""
                    else:
                        actualizado = ""

                    devices.append({
                        'id': id, 
                        'placa': placa,
                        'modelo': modelo, 
                        'categoria': categoria,
                        'actualizado': actualizado,
                        'estado': estado
                    })
                
                return JsonResponse({'dispositivo': devices})
            else:
                return JsonResponse({'error': 'Error al obtener las posiciones de Traccar'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No está autorizado para acceder a esta información'}, status=401)
    except Exception as e:
        # Capturar errores no controlados y enviar un mensaje de error
        return JsonResponse({'error': str(e)})

def tracking(request):
    api_url = settings.TRACCAR_URL_BASE + '/api/session'
    
    queryParams = {
        'token': settings.API_TOKEN
    }
    
    encodedParams = urllib.parse.urlencode(queryParams)
    
    url = f'{api_url}?{encodedParams}'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        coordenadas = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
        }
        return coordenadas
        # return JsonResponse({"data": coordenadas})

    else:
        return {'status': 'error'}

# @api_view(['POST'])
def formatear_decimales(valor):
    return "{:.2f}".format(valor)

def formatear_distancia(distancia):
    return "{:.2f} metros".format(distancia)

def obtener_formato_tiempo(segundos):
    horas, resto = divmod(segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{int(horas)}h {int(minutos)}m {int(segundos)}s"

def get_history_gps(deviceId):
    dispositivo = deviceId

    # Definir zona horaria UTC
    tz_utc = pytz.UTC
    tz_utc_minus_5 = pytz.timezone('America/Bogota')  # Cambiar según sea necesario para UTC-5

    # Fecha actual en UTC
    fecha_actual = datetime.datetime.now(tz=tz_utc).date()

    # Establecer inicio con la fecha actual en UTC (00:00:01)
    inicio = datetime.datetime.combine(fecha_actual, datetime.time(0, 0, 1), tzinfo=tz_utc)
    fin = datetime.datetime.now(tz=tz_utc)

    # Convertir a formato ISO con 'Z' (indicador de UTC)
    inicio_str = inicio.isoformat().replace("+00:00", "Z")
    fin_str = fin.isoformat().replace("+00:00", "Z")

    api_url = settings.TRACCAR_URL_BASE + '/api/positions'

    # Parámetros para la API
    encodedParams = {
        "deviceId": dispositivo,
        "from": inicio_str,
        "to": fin_str
    }

    # Solicitud a la API
    response = requests.get(api_url, params=encodedParams, auth=(settings.API_USR_TRACCAR, settings.API_PSS_TRACCAR))

    if response.status_code == 200:
        data = response.json()

        registros = []
        ultima_posicion = None 
        ultima_posicion_distancia = None

        for posicion in data:
            velocidad = posicion.get('speed')
            motion = posicion['attributes']['motion']
            fecha_hora_utc = posicion.get('deviceTime')

            # Convertir la fecha desde UTC a UTC-5
            prefecha_utc = datetime.datetime.strptime(fecha_hora_utc, '%Y-%m-%dT%H:%M:%S.%f%z')
            prefecha_utc_minus_5 = prefecha_utc.astimezone(tz_utc_minus_5)
            fecha_formateada = prefecha_utc_minus_5.strftime('%Y-%m-%d %H:%M:%S')

            tiempo_detenido = 0
            if motion:
                evento = 'Movimiento'
            else:
                evento = 'Detenido'

            if velocidad == 0:
                tiempo_actual = prefecha_utc
                if ultima_posicion:
                    tiempo_detenido = (tiempo_actual - ultima_posicion).total_seconds()
                ultima_posicion = tiempo_actual

            distancia_recorrida = 0.0
            if ultima_posicion_distancia:
                coordenadas_actual = (posicion.get('latitude'), posicion.get('longitude'))
                coordenadas_anterior = (ultima_posicion_distancia.get('latitude'), ultima_posicion_distancia.get('longitude'))
                distancia_recorrida = geodesic(coordenadas_anterior, coordenadas_actual).meters

            posicion['tiempo_detenido'] = obtener_formato_tiempo(tiempo_detenido)
            posicion['distancia_recorrida'] = distancia_recorrida

            history = {
                "motion": motion,
                "evento": evento,
                "velocidad": formatear_decimales(velocidad) + " Km/h",
                "latitud": posicion.get('latitude'),
                "longitud": posicion.get('longitude'),
                "fecha": fecha_formateada,  # Fecha en UTC-5
                "distancia": formatear_distancia(distancia_recorrida),
                "tiempoDetenido": posicion['tiempo_detenido']
            }
            registros.append(history)
            ultima_posicion_distancia = posicion

        return JsonResponse({"registros": registros})

    return JsonResponse({"error": "Ocurrió un error en la conexión"}, status=500)

def obtener_formato_tiempo(segundos):
    if segundos is None:
        return None

    td = datetime.timedelta(seconds=segundos)
    
    if segundos < 60:
        return f"{segundos} segundos"
    elif segundos < 3600:
        minutos = td.seconds // 60
        segundos_restantes = td.seconds % 60
        return f"{minutos} minutos {segundos_restantes} segundos"
    else:
        horas = td.seconds // 3600
        minutos_restantes = (td.seconds % 3600) // 60
        segundos_restantes = (td.seconds % 3600) % 60
        return f"{horas} horas {minutos_restantes} minutos {segundos_restantes} segundos"

def formatear_distancia(valor):
    if isinstance(valor, (int, float)):
        if valor > 999.99:
            valor = valor / 1000  # Convertir a kilómetros
            valor_formateado = formatear_decimales(valor)
            return "{} Km".format(valor_formateado)
        else:
            valor_formateado = formatear_decimales(valor)
            return "{} m".format(valor_formateado)
    elif isinstance(valor, str) and valor.isdigit():
        valor_num = float(valor)
        if valor_num > 999.99:
            valor_num = valor_num / 1000  # Convertir a kilómetros
            valor_formateado = formatear_decimales(valor_num)
            return "{} Km".format(valor_formateado)
        else:
            valor_formateado = formatear_decimales(valor_num)
            return "{} m".format(valor_formateado)
    else:
        return "0.0 m"
    
def formatear_decimales(valor):
    if isinstance(valor, (int, float)):
        return "{:.2f}".format(valor)
    elif isinstance(valor, str) and valor.isdigit():
        return "{:.2f}".format(float(valor))
    else:
        return 0



