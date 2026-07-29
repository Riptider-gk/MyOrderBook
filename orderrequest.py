from pydantic import BaseModel

class OrderRequest (BaseModel):
    side: str
    price: int
    quantity: int