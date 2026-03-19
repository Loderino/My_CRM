from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from CRM.database.repositories import ClientRepository, OrderRepository
from CRM.server.api.dependencies import get_repository

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    client_repo: ClientRepository = Depends(get_repository(ClientRepository)),
    order_repo: OrderRepository = Depends(get_repository(OrderRepository))
    ):
    active_orders = await order_repo.get_active_orders()

    return request.app.state.templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "title": "Главная - CRM",
            "total_earned": 127.5,
            "recent_orders": active_orders,
            "deadlines": [...]
        }
    )