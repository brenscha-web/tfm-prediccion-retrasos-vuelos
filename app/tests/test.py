import requests

url = 'http://localhost:8099/predict'

vuelo_ejemplo = {
    'origen': 'FLL',
    'destino': 'ATL',
    'aerolinea': 'B6',
    'distancia': 581,
    'hora': 18,
    'temperatura_c': 29.5,
    'punto_rocio_c': 24.0,
    'viento_ms': 14.5,
    'visibilidad_m': 9000,
    'precipitacion_mm': 6.5,
    'temporada_alta': 1,
    'franja_horaria_enc': 3,
    'bin_visibilidad_enc': 2,
    'bin_precipitacion_enc': 2,
}

respuesta = requests.post(url, json=vuelo_ejemplo)
print("Código de estado:", respuesta.status_code)
print("Contenido de la respuesta:")
print(respuesta.text)