import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuración
NUM_SAMPLES = 10000
RUTAS = [1, 2, 3, 4, 5]

data = []

print("Generando datos falsos con formato Timestamp...")

start_date = datetime(2025, 1, 1)

for _ in range(NUM_SAMPLES):
    # Generar timestamp aleatorio en el año 2025
    random_days = random.randint(0, 364)
    random_seconds = random.randint(0, 86399)
    current_datetime = start_date + timedelta(days=random_days, seconds=random_seconds)
    
    timestamp_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    hora = current_datetime.hour
    
    ruta = random.choice(RUTAS)
    
    # Lógica de generación de datos basada en la hora
    # Picos a las 8am y 6pm (18:00)
    
    base_autos = 10
    base_personas = 2
    
    if 7 <= hora <= 9:
        base_autos += 30 # Hora pico mañana
        base_personas += 5
    elif 17 <= hora <= 19:
        base_autos += 40 # Hora pico tarde
        base_personas += 8
    elif 10 <= hora <= 16:
        base_autos += 15 # Tráfico medio dia
        base_personas += 3
    else:
        base_autos += 2 # Noche/Madrugada
        base_personas += 0
        
    # Variación aleatoria
    autos = base_autos + random.randint(-5, 15)
    personas = base_personas + random.randint(-2, 5)
    
    # Factor de ruta
    if ruta == 1: # Autopista Duarte (Más autos)
        autos += 10
    elif ruta == 4: # Winston Churchill (Más personas)
        personas += 5
        
    # Asegurar no negativos
    autos = max(0, autos)
    personas = max(0, personas)
    
    data.append([timestamp_str, ruta, personas, autos])

# El formato solicitado es Timestamp, Ruta (agregada para poder predecir por ruta), Personas, Autos
# NOTA: El usuario pidió "Timestamp,Personas,Autos" en el ejemplo, pero necesitamos la RUTA para predecir
# Si el usuario quiere predecir tráfico en una ruta específica, necesitamos incluir la ruta en los datos.
# Voy a incluir la ruta como columna adicional para mantener la funcionalidad de la app.

df = pd.DataFrame(data, columns=['Timestamp', 'Ruta', 'Personas', 'Autos'])
output_path = 'Predicciones/trafico_falso.csv'
df.to_csv(output_path, index=False)
print(f"Archivo CSV generado en: {output_path}")
