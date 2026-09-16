import requests

url = 'http://localhost:8099/predict'

vuelo_buen_tiempo = {
    'origen': 'LAS',
    'destino': 'PHX',
    'aerolinea': 'DL',
    'distancia': 256,
    'hora': 6,
    'temperatura_c': 18.0,
    'punto_rocio_c': 5.0,
    'viento_ms': 3.0,
    'visibilidad_m': 16000,
    'precipitacion_mm': 0.0,
    'temporada_alta': 0,
    'franja_horaria_enc': 1,      # Mañana
    'bin_visibilidad_enc': 3,     # Buena
    'bin_precipitacion_enc': 0,   # Sin lluvia
}

respuesta = requests.post(url, json=vuelo_buen_tiempo)
print("Código de estado:", respuesta.status_code)
print("Contenido de la respuesta:")
print(respuesta.text)