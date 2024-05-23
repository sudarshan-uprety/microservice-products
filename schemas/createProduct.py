from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    image: str
    category: str
    stock: int
    status: bool
    vendor: str