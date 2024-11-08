from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import numpy as np
import time
from threading import Event

app = APIRouter()

# Tamaño de la placa y parámetros de simulación
WIDTH, HEIGHT = 100, 100  # Tamaño de la placa (ajustable)
k = 0.01  # Constante de enfriamiento
ambient_temperature = 25  # Temperatura ambiente en grados Celsius
blowtorch_temperature = 200  # Temperatura del soplete en grados Celsius
blowtorch_position = (50, 50)  # Posición inicial del soplete
temperature_grid = np.full((WIDTH, HEIGHT), ambient_temperature)

# Variables de control de la simulación
simulation_running = Event()
simulation_paused = Event()

class ConfigParams(BaseModel):
    k: float
    blowtorch_temperature: float
    ambient_temperature: float
    blowtorch_position: tuple[int, int]

@app.on_event("startup")
async def initialize_simulation():
    simulation_paused.set()  # Inicia en pausa por defecto

@app.post("/start")
async def start_simulation(background_tasks: BackgroundTasks):
    simulation_running.set()
    simulation_paused.clear()
    background_tasks.add_task(run_simulation)
    return {"message": "Simulación iniciada"}

@app.get("/temperature")
async def get_temperature():
    # Convierte el array de temperatura en una lista para enviarlo como JSON
    return {"temperature_grid": temperature_grid.tolist()}

@app.post("/pause")
async def pause_simulation():
    simulation_paused.set()
    return {"message": "Simulación pausada"}

@app.post("/reset")
async def reset_simulation():
    global temperature_grid
    temperature_grid = np.full((WIDTH, HEIGHT), ambient_temperature)
    simulation_running.clear()
    simulation_paused.set()
    return {"message": "Simulación reiniciada"}

@app.post("/config")
async def configure_simulation(params: ConfigParams):
    global k, blowtorch_temperature, ambient_temperature, blowtorch_position
    k = params.k
    blowtorch_temperature = params.blowtorch_temperature
    ambient_temperature = params.ambient_temperature
    blowtorch_position = params.blowtorch_position
    return {"message": "Parámetros actualizados"}

def run_simulation():
    global temperature_grid
    while simulation_running.is_set():
        if simulation_paused.is_set():
            time.sleep(1)  # Espera si la simulación está pausada
            continue
        # Aplicar calor en la posición del soplete
        x, y = blowtorch_position
        temperature_grid[x, y] = blowtorch_temperature
        
        # Calcula la transferencia de calor en la placa
        new_grid = temperature_grid.copy()
        for i in range(1, WIDTH - 1):
            for j in range(1, HEIGHT - 1):
                new_grid[i, j] = (
                    temperature_grid[i, j] +
                    k * (
                        temperature_grid[i+1, j] +
                        temperature_grid[i-1, j] +
                        temperature_grid[i, j+1] +
                        temperature_grid[i, j-1] -
                        4 * temperature_grid[i, j]
                    )
                )
        temperature_grid = new_grid
        time.sleep(0.1)  # Intervalo de actualización de la simulación
