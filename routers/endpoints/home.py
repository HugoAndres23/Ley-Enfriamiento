from fastapi import APIRouter, Request
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
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

@app.get("/")
async def home(request: Request):
    image_base64 = crear_grafico(placa)

    return TEMPLATES.TemplateResponse("index.j2", {
        "request": request,
        "image_base64": image_base64,
        "soplete": soplete
    })

@app.post("/aplicar_soplete")
async def configurar_soplete(config: SopleteConfig):
    soplete.temperatura = config.temperatura
    if soplete.temperatura and soplete.temperatura > placa.temperatura[soplete.posicion]:
        placa.aplicar_soplete(soplete, 100)
        # placa.disipacion += 0.1

    image_base64 = crear_grafico(placa)
    return {"message": "Configuración del soplete aplicada.", "image": image_base64}


def crear_grafico(placa: Placa):
    fig, ax = plt.subplots()
    cmap = LinearSegmentedColormap.from_list("temp_cmap", ["blue", "cyan", "green", "yellow", "orange", "red"])
    heatmap = ax.imshow(placa.temperatura, cmap=cmap, vmin=placa.temperatura_ambiente, vmax=500)
    plt.colorbar(heatmap, ax=ax, orientation="vertical")

    ax.set_xticks([])
    ax.set_yticks([])

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
