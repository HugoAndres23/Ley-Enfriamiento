from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()
TEMPLATES = Jinja2Templates(directory="routers/templates")
router.mount('/static', StaticFiles(directory='.\.\static'), name='static')


@router.get("/static/{directoryname}/{filename}")
def get_static_file(request: Request, directoryname: str, filename: str):
    return FileResponse(f"static/{directoryname}/{filename}")