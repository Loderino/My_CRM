from typing import Optional
from pydantic import BaseModel

class OrderRequest(BaseModel):
    client_id: int
    title: str
    description: Optional[str]
    instruments: list[str]
    contract_price: int