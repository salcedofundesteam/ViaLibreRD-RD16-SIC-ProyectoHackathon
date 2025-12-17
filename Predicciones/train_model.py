import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os
from datetime import datetime

print("Cargando datos...")
df = pd.read_csv('Predicciones/trafico_falso.csv')

# Preprocesamiento: Extraer hora del Timestamp
# Convertir Timestamp a datetime objects
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['hora'] = df['Timestamp'].dt.hour

# Definir Features (X) y Target (y)
# Features: Ruta, Hora
# Target: Autos (usaremos 'Autos' como proxy del nivel de tráfico)
# Podríamos combinar Autos + Personas para una métrica de congestión, 
# pero por ahora usaremos Autos como el indicador principal de "Tráfico".
# O mejor, creemos una columna 'Congestion' que normalice un poco esto.

# Normalizamos 'Autos' a una escala aproximada de 0-100 para mantener consistencia con la app
# Asumiendo que max autos es alrededor de 80-100 en los datos generados
max_autos = df['Autos'].max()
df['Congestion'] = (df['Autos'] / max_autos) * 100

X = df[['Ruta', 'hora']]
y = df['Congestion']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Entrenando modelo...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}")

# Guardar modelo
model_path = 'Predicciones/modelo_trafico.joblib'
joblib.dump(model, model_path)
print(f"Modelo guardado en: {model_path}")
