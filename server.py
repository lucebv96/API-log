from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()

VALID_API_KEYS = ["123", "456", "789", "1011"]

class Log(BaseModel):
    timestamp: str
    service_name: str
    log_level: str
    message: str

def iniciar_db():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            received_at TEXT,
            service_name TEXT,
            log_level TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def guardar_log(timestamp, service_name, log_level, message):
    received_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, received_at, service_name, log_level, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, received_at, service_name, log_level, message))
    conn.commit()
    conn.close()

@app.post("/logs")
async def log(log: Log, authorization: str = Header(None)):
    if authorization not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    guardar_log(log.timestamp, log.service_name, log.log_level, log.message)
    return {"status": "success"}

@app.get("/logs")
async def obtener_logs(start_date: str = None, end_date: str = None,
                       start_received_at: str = None, end_received_at: str = None):
    consulta = "SELECT * FROM logs WHERE 1=1"
    parametros = []
    if start_date:
        consulta += " AND timestamp >= ?"
        parametros.append(start_date)
    if end_date:
        consulta += " AND timestamp <= ?"
        parametros.append(end_date)
    if start_received_at:
        consulta += " AND received_at >= ?"
        parametros.append(start_received_at)
    if end_received_at:
        consulta += " AND received_at <= ?"
        parametros.append(end_received_at)

    consulta += " ORDER BY timestamp ASC, received_at ASC"  # Ordena por timestamp y luego por received_at

    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute(consulta, parametros)
    logs = cursor.fetchall()
    conn.close()

    lista_de_logs = []
    for log in logs:
        lista_de_logs.append({
            "id": log[0],
            "timestamp": log[1],
            "received_at": log[2],
            "service_name": log[3],
            "log_level": log[4],
            "message": log[5]
        })

    return lista_de_logs


if __name__ == "__main__":
    iniciar_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
