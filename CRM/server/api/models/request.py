from pydantic import BaseModel

class OrderRequest(BaseModel):
    client_id: int
    title: str
    description: str | None = None
    instruments: list[str] = []
    contract_price: int