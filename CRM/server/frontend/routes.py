from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, Query
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

@router.get("/clients", response_class=HTMLResponse)
async def clients(
    request: Request,
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Записей на странице"),
    search: Optional[str] = Query(None, description="Поиск по имени/контактам"),
    orders: str = Query("all", description="Фильтр по заказам: all, with_orders, without_orders"),
    client_repo: ClientRepository = Depends(get_repository(ClientRepository))
):
    print(await client_repo.get_all())
    filters = {}
    # Фильтр по наличию заказов
    if orders != "all":
        filters["has_orders"] = (orders == "with_orders")
    
    # Поиск по тексту
    if search:
        filters["search"] = search
    
    # Получаем данные с пагинацией
    skip = (page - 1) * per_page
    clients, total = await client_repo.get_filtered(
        skip=skip,
        limit=per_page,
        **filters
    )
    
    # Для каждого клиента считаем статистику по заказам
    for client in clients:
        stats = await client_repo.get_order_stats(client.id)
        client.orders_count = stats["orders_count"]
        client.orders_sum = stats["orders_sum"]
    
    return request.app.state.templates.TemplateResponse(
        "pages/clients/index.html",
        {
            "request": request,
            "clients": clients,
            "total_clients": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "search_query": search or "",
            "orders_filter": orders
        }
    )

@router.get("/clients/create", response_class=HTMLResponse)
async def create_client_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "pages/clients/create.html",
        {"request": request}
    )

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
        if v.strip():
            contacts[t] = v.strip()

    await client_repo.create(
        name=name,
        contacts=contacts,
        notes=notes
    )
    # Перенаправляем на страницу клиента или список
    return RedirectResponse(url="/clients", status_code=303)


@router.get("/orders", response_class=HTMLResponse)
async def orders_list(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    order_repo: OrderRepository = Depends(get_repository(OrderRepository))
):
    skip = (page - 1) * per_page
    
    # Получаем заказы с пагинацией
    orders, total = await order_repo.get_filtered(
        skip=skip,
        limit=per_page,
        search=search
    )
    
    # Для каждого заказа подгружаем клиента
    for order in orders:
        await order_repo.session.refresh(order, attribute_names=['client'])
    
    return request.app.state.templates.TemplateResponse(
        "pages/orders/index.html",
        {
            "request": request,
            "orders": orders,
            "total_orders": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "search_query": search or "",
            "today": datetime.now().date(),
            "timedelta": timedelta
        }
    )