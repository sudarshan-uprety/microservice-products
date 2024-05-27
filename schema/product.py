from pydantic import BaseModel


class ProductCreate(BaseModel):
    """schema for product model"""
    name: str
    price: float
