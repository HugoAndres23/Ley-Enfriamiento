from fastapi import APIRouter, Request
import matplotlib.pyplot as plt
import io
import base64
from pydantic import BaseModel

from routers.endpoints.app import Soplete, Placa
from routers.endpoints.static import TEMPLATES

app = APIRouter()

soplete = Soplete()
placa = Placa()

class SopleteConfig(BaseModel):
    temperatura: float
    posicion: tuple
    radio: int

@app.get("/")
async def home(request: Request):
    image_base64 = crear_grafico(placa)

    return TEMPLATES.TemplateResponse("index.j2", {
        "request": request,
        "image_base64": image_base64,
        "soplete": soplete,
        "placa": placa
    })

@app.post("/aplicar_soplete")
async def configurar_soplete(request: Request, config: SopleteConfig):
    soplete.radio = config.radio
    soplete.temperatura = config.temperatura
    soplete.posicion = config.posicion
    if soplete.temperatura and soplete.temperatura > placa.temperatura[soplete.posicion]:
        placa.aplicar_soplete(soplete)
    else:
        placa.enfriar_lentamente()

    image_base64 = crear_grafico(placa)
    return {"table": TEMPLATES.get_template("table_temps.j2").render({
        "request": request,
        "soplete": soplete,
        "placa": placa,
    }),
    "image": image_base64}


def crear_grafico(placa: Placa):
    fig, ax = plt.subplots()
    heatmap = ax.imshow(placa.temperatura, cmap='hot', origin="lower", vmin=placa.temperatura_ambiente, vmax=200)
    plt.colorbar(heatmap, ax=ax, orientation="vertical", label='Temperatura')

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")