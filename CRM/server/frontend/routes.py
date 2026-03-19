from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse

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

@router.get("/clients/create", response_class=HTMLResponse)
async def create_client_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "pages/clients/create.html",
        {"request": request}
    )

# Обработка формы
@router.post("/clients/create")
async def create_client(
    request: Request,
    name: str = Form(...),
    contact_type: list[str] = Form([]),
    contact_value: list[str] = Form([]),
    notes: str = Form(""),
    client_repo: ClientRepository = Depends(get_repository(ClientRepository))
    ):
    contacts = {}
    for t, v in zip(contact_type, contact_value):
        if v.strip():  # только непустые
            contacts[t] = v.strip()

    # Создаём клиента
    client = await client_repo.create(
        name=name,
        contacts=contacts,
        notes=notes
    )

    # Перенаправляем на страницу клиента или список
    return RedirectResponse(url="/clients", status_code=303)