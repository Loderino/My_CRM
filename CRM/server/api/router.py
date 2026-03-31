from fastapi import APIRouter

from .routes import clients_router, orders_router

api_router = APIRouter()
api_router.include_router(clients_router, prefix="/clients")
api_router.include_router(orders_router, prefix="/orders")
