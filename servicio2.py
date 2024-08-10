import requests
from datetime import datetime
import random
import time

# URL del servidor FastAPI
SERVER_URL = "http://localhost:8000/logs"

# Lista de API Keys, incluyendo una inválida
API_KEYS = ["123", "456", "789", "1011", "000"]  # "000" es la API key no válida

# Nombres de servicios simulados
SERVICES = ["Service1", "Service2", "Service3"]

def generar_log():
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    service_name = random.choice(SERVICES)
    log_level = random.choice(["INFO", "ERROR", "DEBUG"])
    message = "Este es un log de prueba de Servicio2"
    return {
        "timestamp": timestamp,
        "service_name": service_name,
        "log_level": log_level,
        "message": message
    }

def enviar_log():
    log_data = generar_log()
    api_key = random.choice(API_KEYS)  # Selecciona una API key de manera aleatoria
    headers = {
        "Authorization": api_key,  # Envía la API key en el encabezado
        "Content-Type": "application/json"  # Especifica que el contenido es JSON
    }
    response = requests.post(SERVER_URL, json=log_data, headers=headers)

    if response.status_code == 200:
        print(f"Log enviado exitosamente con API key '{api_key}': {log_data}")
    else:
        print(f"Error al enviar el log con API key '{api_key}': {response.status_code} - {response.text}")

if __name__ == "__main__":
    while True:
        enviar_log()
        time.sleep(random.randint(1, 5))  # Espera aleatoria entre 1 y 5 segundos antes de enviar el siguiente log
