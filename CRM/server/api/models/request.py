from datetime import datetime
from pydantic import BaseModel

class OrderRequest(BaseModel):
    client_id: int
    title: str
    description: str | None = None
    instruments: list[str] = []
    contract_price: int
    deadline_date: datetime | None = None

class OrderUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    contract_price: int | None = None
    deadline_date: datetime | None = None
    instruments: list[str] | None = None
    status: str | None = None
    progress: int | None = None

class ClientRequest(BaseModel):
    name: str
    contacts: dict[str, str] | None = None
    notes: str | None = None

class ClientUpdateRequest(BaseModel):
    name: str | None = None
    contacts: dict[str, str] | None = None
    notes: str | None = None