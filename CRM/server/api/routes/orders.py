from typing import Literal
from fastapi import APIRouter, Depends, Body

from CRM.database.models import OrderStatus
from CRM.database.services.order_service import OrderService
from CRM.server.api.dependencies import get_service
from CRM.server.api.models.request import OrderRequest
from CRM.server.api.models.response import OrderResponse, DetailedOrderResponse, StatusLogResponse, ProgressLogResponse

orders_router = APIRouter()

@orders_router.get("/")
async def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    order_by: Literal["id", "title", "created_date", "deadline_date", "contract_price", "client_id"] = "id",
    order_service: OrderService = Depends(get_service(OrderService))
    ) -> list[OrderResponse]:
    return await order_service.get_all_orders(skip, limit, order_by)

@orders_router.get("/{order_id}")
async def get_order(
    order_id: int,
    order_service: OrderService = Depends(get_service(OrderService))
    ) -> DetailedOrderResponse:
    return await order_service.get_order(order_id)

@orders_router.post("/")
async def create_order(
    order: OrderRequest,
    order_service: OrderService = Depends(get_service(OrderService))
    ) -> OrderResponse:
    return await order_service.create_order(order.model_dump())

@orders_router.get("/{order_id}/status")
async def get_order_current_status(
    order_id: int,
    order_service: OrderService = Depends(get_service(OrderService))
    ) -> StatusLogResponse:
    return await order_service.get_order_current_status(order_id)

@orders_router.post("/{order_id}/status")
async def update_order_status(
    order_id: int,
    new_status: Literal[OrderStatus.CREATED, OrderStatus.IN_PROGRESS, OrderStatus.TESTING, OrderStatus.READY, OrderStatus.COMPLETED, OrderStatus.CANCELLED],
    order_service: OrderService = Depends(get_service(OrderService))
    ) -> StatusLogResponse:
    return await order_service.create_status(order_id, new_status)

@orders_router.get("/{order_id}/progress")
async def get_order_current_progress(
    order_id: int,
    order_service: OrderService = Depends(get_service(OrderService))
    ) -> ProgressLogResponse:
    return await order_service.get_order_current_progress(order_id)

@orders_router.post("/{order_id}/progress")
async def update_order_progress(
    order_id: int,
    percentage: int = Body(..., ge=0, le=100),
    order_service: OrderService = Depends(get_service(OrderService))
    ) -> StatusLogResponse:
    return await order_service.create_progress(order_id, percentage)