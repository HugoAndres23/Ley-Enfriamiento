import numpy as np
from fastapi import APIRouter, Request
from routers.endpoints.static import TEMPLATES

app = APIRouter()

@app.get("/")
async def read_home(request: Request):
    # Genera datos iniciales de la temperatura (si quieres mostrar un estado inicial)
    initial_temperature = np.full((10, 10), 25).tolist()  # Array inicial de temperatura
    return TEMPLATES.TemplateResponse("index.j2", {
        "request": request,
        "initial_temperature": initial_temperature
    })
