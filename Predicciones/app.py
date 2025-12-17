import joblib
import pandas as pd
import os

MODEL_PATH = 'Predicciones/modelo_trafico.joblib'

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: No se encontró el modelo en {MODEL_PATH}")
        print("Por favor, ejecuta primero train_model.py")
        return

    print("Cargando modelo de predicción de tráfico...")
    model = joblib.load(MODEL_PATH)
    print("Modelo cargado exitosamente.")
    print("-" * 30)

    RUTAS = {
        1: "Autopista Duarte",
        2: "Avenida 27 de Febrero",
        3: "Avenida John F. Kennedy",
        4: "Avenida Winston Churchill",
        5: "Avenida Máximo Gómez"
    }

    try:
        print("\nSeleccione la ruta:")
        for key, value in RUTAS.items():
            print(f"{key}. {value}")
            
        ruta_input = input("\nIngrese el número de la ruta (1-5): ")
        ruta = int(ruta_input)
        
        hora_input = input("Seleccione la hora (0-23): ")
        hora = int(hora_input)
        
        if ruta not in RUTAS:
            print("Error: La ruta debe estar entre 1 y 5.")
            return
            
        if not (0 <= hora <= 23):
            print("Error: La hora debe estar entre 0 y 23.")
            return

        input_data = pd.DataFrame([[ruta, hora]], columns=['Ruta', 'hora'])
        
        prediction = model.predict(input_data)[0]
        
        print("-" * 30)
        print(f"Predicción de tráfico para {RUTAS[ruta]} a las {hora}:00 horas:")
        print(f"Porcentaje de congestión esperado: {int(prediction)}%")
        
        if prediction > 80:
            print("Estado: Muy Congestionado")
        elif prediction > 50:
            print("Estado: Tráfico Moderado")
        else:
            print("Estado: Tráfico Fluido")
            
    except ValueError:
        print("Error: Por favor ingrese números válidos.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
