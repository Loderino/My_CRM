from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "title": "Главная - CRM",
            "total_earned": 127.5,
            "recent_orders": [...],
            "deadlines": [...]
        }
    )