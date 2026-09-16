#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install nest_asyncio


# In[ ]:


import pickle
import pandas as pd
from flask import Flask, request, jsonify
import nest_asyncio


# # 8.2 Aplicación Flask — servicio de predicción de retrasos

# In[ ]:


# Carga del modelo y de los encoders
modelo = pickle.load(open('../modelo/modelo_retrasos.pkl', 'rb'))
encoders = pickle.load(open('../modelo/encoders_retrasos.pkl', 'rb'))

app = Flask(__name__)

def prepare_data(flight):
    """Converts raw flight data into the format expected by the model."""
    row = {
        'DISTANCE': flight['distancia'],
        'hora': flight['hora'],
        'temperatura_c': flight['temperatura_c'],
        'punto_rocio_c': flight['punto_rocio_c'],
        'viento_ms': flight['viento_ms'],
        'visibilidad_m': flight['visibilidad_m'],
        'precipitacion_mm': flight['precipitacion_mm'],
        'viento_fuerte': 1 if flight['viento_ms'] > 12.9 else 0,
        'temporada_alta': flight['temporada_alta'],
        'indice_congestion': flight.get('indice_congestion', 20),
        'franja_horaria_enc': flight['franja_horaria_enc'],
        'bin_visibilidad_enc': flight['bin_visibilidad_enc'],
        'bin_precipitacion_enc': flight['bin_precipitacion_enc'],
        'OP_UNIQUE_CARRIER_target_enc': encoders['carrier']['mapa'].get(
            flight['aerolinea'], encoders['carrier']['media_global']),
        'IATA_target_enc': encoders['iata']['mapa'].get(
            flight['origen'], encoders['iata']['media_global']),
        'DEST_target_enc': encoders['dest']['mapa'].get(
            flight['destino'], encoders['dest']['media_global']),
    }
    return pd.DataFrame([row])[encoders['columns_modelo']]


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        model_row = prepare_data(data)

        probabilities = model.predict_proba(model_row)
        probability = float(probabilities[0][1]) # Standard array/list access

        prediction = int(probability >= encoders['umbral_decision'])

        return jsonify({
            'delay_probability': round(probability, 3),
            'prediction': 'Delayed' if prediction == 1 else 'On time',
            'threshold_used': encoders['umbral_decision']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8099)#, debug=False, use_reloader=False)


# In[ ]:




