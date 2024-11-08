from fastapi import FastAPI
from routers.endpoints.home import router as home
from routers.endpoints.static import router as static
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(home)
app.include_router(static)
