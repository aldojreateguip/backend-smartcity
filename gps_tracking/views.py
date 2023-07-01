from django.http import JsonResponse
from .teltonika_decoder import decode_teltonika_message,decode_teltonika_messagebase

def receive_gps_data(request):
    encoded_message = request.body  # Obtener el mensaje codificado del cuerpo de la solicitud
    print(encoded_message)
    if len(encoded_message) < 18:
        return JsonResponse({"error": "Mensaje codificado inválido."})
    # Decodificar el mensaje Teltonika
    decoded_data = decode_teltonika_message(encoded_message)
    #version 2
    decoded_data_base = decode_teltonika_messagebase(encoded_message)
    
    # Realizar el procesamiento adicional o almacenamiento según tus necesidades
    # ...
    
    # Devolver una respuesta apropiada
    response_data = {
        'message': 'Datos GPS recibidos exitosamente.',
        'data': decoded_data,
        'data2': decoded_data_base
    }
    return JsonResponse(response_data)
