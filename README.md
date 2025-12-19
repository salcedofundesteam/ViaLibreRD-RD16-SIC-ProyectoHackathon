# Sistema de Control de Tráfico

Proyecto sencillo para:
- Detectar personas y vehículos con OpenCV.
- Seguir vehículos y estimar su velocidad.
- Manejar un semáforo que alterna cada 10 segundos (empieza en verde).
- Guardar capturas si hay autos en rojo.
- Enviar alertas por exceso de velocidad por correo (máximo una cada 4 segundos).
- Registrar métricas en CSV y visualizar gráficas.
- Predecir congestión por ruta y hora con un modelo entrenado.

## Requisitos
- Python 3.10 o superior.
- Instalar dependencias:
```
pip install -r requirements.txt
```

## Uso rápido
- Ejecutar el sistema principal:
```
python main.py
```
Presiona `q` para cerrar la ventana.

- Visualizar datos guardados:
```
python visualizar_datos.py
```
Genera `data/grafico_trafico.png`.

- Predicciones (ML):
```
python Predicciones/train_model.py   # entrenar modelo (usa trafico_falso.csv)
python Predicciones/app.py          # CLI para predecir por ruta y hora
```

## Configuración
- Edita `modules/config.py`:
  - `VIDEO_PATH`: archivo de video de entrada.
  - `FULLBODY_CASCADE_PATH` y `CAR_CASCADE_PATH`: clasificadores Haar.
  - `DATA_FILE_PATH`: CSV de salida para métricas.
  - `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECIPIENT`: credenciales de correo.
- Consejos:
  - Usa contraseñas de aplicación para Gmail.
  - Evita subir credenciales reales al repositorio.

## Estructura
```
main.py
modules/
  detectors.py
  tracker.py
  notifications.py
  data_manager.py
  config.py
haarcascades/
videoprueba/
infracciones/
data/
Predicciones/
requirements.txt
README.md
```

## Qué hace cada parte
- `main.py`: abre el video, detecta, sigue vehículos, calcula velocidades, controla el semáforo, guarda capturas y datos.
- `modules/detectors.py`: detecciones con Haar Cascades.
- `modules/tracker.py`: seguimiento de objetos y cálculo de velocidad.
- `modules/notifications.py`: envía correos de alerta.
- `modules/data_manager.py`: guarda métricas en `data/datos_trafico.csv`.
- `visualizar_datos.py`: genera una gráfica con el histórico.
- `Predicciones/`: entrenamiento y uso del modelo de congestión.

## Notas
- El semáforo cambia cada 10 segundos y arranca en verde.
- Las capturas se guardan en `infracciones/` cuando hay autos en rojo.
- El límite actual para enviar alertas por exceso de velocidad es una cada 4 segundos.
- Ajusta `pixels_per_meter` en `tracker.py` si cambias la escena del video.

## Problemas comunes
- No abre el video: revisa `VIDEO_PATH`.
- No cargan los clasificadores: revisa rutas en `haarcascades/`.
- Falla el correo: usa App Passwords y verifica SMTP.
- Gráfica vacía: confirma que `data/datos_trafico.csv` tiene datos.
