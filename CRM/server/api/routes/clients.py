from fastapi import APIRouter, Depends, Query


from CRM.database.services import ClientService
from CRM.server.api.dependencies import get_service
from CRM.server.api.models.request import ClientUpdateRequest, ClientRequest
from CRM.server.api.models.response import ClientResponse

clients_router = APIRouter()

@clients_router.get("/")
async def get_all_clients(
    client_service: ClientService = Depends(get_service(ClientService))
) -> list[ClientResponse]:
    return await client_service.get_all_clients()

@clients_router.get("/search")
async def search_clients(
    q: str = Query(..., min_length=2),
    client_service: ClientService = Depends(get_service(ClientService))
):
    clients = await client_service.search_clients(q)
    return clients

@clients_router.get("/{client_id}")
async def get_client(
    client_id: int,
    client_service: ClientService = Depends(get_service(ClientService))
) -> ClientResponse:
    return await client_service.get_client(client_id)

@clients_router.post("/")
async def create_client(
    client_data: ClientRequest,
    client_service: ClientService = Depends(get_service(ClientService))
) -> ClientResponse:
    return await client_service.create_client(**client_data.model_dump())

@clients_router.patch("/{client_id}")
async def update_client(
    client_id: int,
    data: ClientUpdateRequest,
    client_service: ClientService = Depends(get_service(ClientService))
) -> ClientResponse:
    update_data = data.model_dump(exclude_none=True)
    return await client_service.update_client(client_id, **update_data)