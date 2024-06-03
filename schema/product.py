from pydantic import BaseModel, validator
from models.category import Category


class ProductCreate(BaseModel):
    """schema for product model"""
    name: str
    price: float
    description: str
    image: str
    category: str
    stock: int
    status: bool
    size: str
    color: str

    @validator('category')
    def validate_category(cls, value):
        category = Category.objects.get(id=value)
        return category
