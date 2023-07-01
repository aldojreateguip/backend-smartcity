import struct
import base64
import binascii

def decode_teltonika_message(encoded_message):
    # Decodificar el mensaje Teltonika
    data = bytearray(encoded_message)
    
    # Leer los campos de encabezado
    codec_id = data[0]  # Identificador del códec
    avl_data_count = data[1]  # Cantidad de datos AVL
    
    # Decodificar los datos AVL
    offset = 2  # Desplazamiento inicial después del encabezado
    
    for _ in range(avl_data_count):
        timestamp = struct.unpack_from("<I", data, offset)[0]  # Marca de tiempo
        priority = data[offset + 4]  # Prioridad
        gps_element = data[offset + 5]  # Elemento GPS
        
        longitude = struct.unpack_from("<i", data, offset + 6)[0] / 10000000  # Longitud
        latitude = struct.unpack_from("<i", data, offset + 10)[0] / 10000000  # Latitud
        
        # ... Decodificar más campos según tus necesidades ...
        
        offset += 18  # Desplazamiento al siguiente conjunto de datos AVL
    
    # ... Realizar el procesamiento adicional según tus necesidades ...
    
    # Devolver los valores decodificados
    return {
        'codec_id': codec_id,
        'avl_data_count': avl_data_count,
        # Agregar más campos decodificados según tus necesidades
    }

def decode_teltonika_messagebase(encoded_message):
    decoded_data = base64.b64decode(encoded_message)  # Decodificar el mensaje codificado en base64
    header = decoded_data[:8]  # Leer el encabezado de 8 bytes
    payload = decoded_data[8:]  # Leer la carga útil
    
    # Decodificar la carga útil en valores individuales
    imei = binascii.hexlify(payload[:8]).decode('utf-8')  # Ejemplo: decodificar IMEI
    latitude = int.from_bytes(payload[8:12], byteorder='big', signed=True) / 10000000  # Ejemplo: decodificar latitud
    longitude = int.from_bytes(payload[12:16], byteorder='big', signed=True) / 10000000  # Ejemplo: decodificar longitud
    speed = payload[16]  # Ejemplo: decodificar velocidad
    
    # ... Realizar el procesamiento adicional según tus necesidades ...
    
    # Devolver los valores decodificados
    return {
        'imei': imei,
        'latitude': latitude,
        'longitude': longitude,
        'speed': speed
    }