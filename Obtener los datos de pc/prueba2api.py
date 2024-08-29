import psutil
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import threading
import time

app = FastAPI()

# Definir un modelo para la información de procesos
class ProcessInfo(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    memory_info: Dict[str, Any]

# Variable global para almacenar la información del sistema
system_data = {}

# Función para obtener la información del sistema
def get_system_info():
    # Información de CPU
    cpu_info = psutil.cpu_percent(interval=1, percpu=True)

    # Información de Memoria
    memory_info = psutil.virtual_memory()._asdict()

    # Información de Disco
    disk_info = psutil.disk_usage('/')._asdict()

    # Información de Red
    net_info = psutil.net_io_counters()._asdict()

    # Información de Procesos
    process_info = get_process_info()

    return {
        "cpu_info": cpu_info,
        "memory_info": memory_info,
        "disk_info": disk_info,
        "net_info": net_info,
        "process_info": process_info
    }

# Función para obtener la información de los procesos
def get_process_info():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:10]  # Mostrar los 10 procesos con mayor uso de CPU

# Función que se ejecuta en un hilo separado para actualizar la información del sistema
def update_system_data():
    global system_data
    while True:
        system_data = get_system_info()
        time.sleep(1)  # Actualiza cada 10 segundos

# Iniciar el hilo de actualización al inicio
update_thread = threading.Thread(target=update_system_data, daemon=True)
update_thread.start()

@app.get("/api/system_info")
async def system_info():
    return system_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
