from fastapi import APIRouter

from .routes import orders_router

api_router = APIRouter()
api_router.include_router(orders_router, prefix="/orders")
