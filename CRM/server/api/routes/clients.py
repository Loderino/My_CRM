from fastapi import APIRouter, Depends, Query


from CRM.database.services import ClientService
from CRM.server.api.dependencies import get_service

clients_router = APIRouter()


@clients_router.get("/search")
async def search_clients(
    q: str = Query(..., min_length=2),
    client_service: ClientService = Depends(get_service(ClientService))
):
    """Поиск клиентов по имени или контактам"""
    print(q)
    clients = await client_service.search_clients(q)
    return clients