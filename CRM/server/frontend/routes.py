from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="CRM/server/frontend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Главная страница CRM
    """
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "CRM для фрилансера",
            "message": "Добро пожаловать!"
        }
    )