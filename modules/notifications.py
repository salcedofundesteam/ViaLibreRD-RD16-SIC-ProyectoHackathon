import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from modules.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT

def send_speeding_alert(vehicle_id, speed, street_name="Avenida Siempre Viva 742"):
    """
    Sends an email alert for a speeding vehicle.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    mensaje = MIMEMultipart()
    mensaje["From"] = EMAIL_SENDER
    mensaje["To"] = EMAIL_RECIPIENT
    mensaje["Subject"] = f"ALERTA DE VELOCIDAD: Vehículo ID {vehicle_id}"
    
    cuerpo = f"""
    ALERTA DE INFRACCIÓN DE TRÁFICO
    --------------------------------
    ID Vehículo: {vehicle_id}
    Velocidad Detectada: {speed:.2f} km/h
    Límite de Velocidad: 70 km/h
    
    Ubicación: {street_name}
    Hora de Infracción: {timestamp}
    
    Este es un mensaje automático del sistema de control de tráfico.
    """
    mensaje.attach(MIMEText(cuerpo, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
            servidor.send_message(mensaje)
        print(f"[CORREO] Alerta enviada para vehículo {vehicle_id} ({speed:.1f} km/h)")
        return True
    except Exception as e:
        print(f"[ERROR CORREO] Fallo al enviar alerta para vehículo {vehicle_id}: {e}")
        return False
