from typing import Optional

from pydantic import BaseModel, validator, Field

from models.category import Category
from models.color import Color
from models.size import Size
from models.type import Type


class ProductCreate(BaseModel):
    """schema for product model"""
    name: str
    price: float
    description: str
    image: str
    category: str
    stock: int
    status: bool
    size: Optional[str] = Field(default=None)
    color: Optional[str] = Field(default=None)
    type: str

    @validator('category')
    def validate_category(cls, value):
        category = Category.objects.get(id=value)
        return category

    @validator('size')
    def validate_size(cls, value):
        size = Size.objects.get(id=value)
        return size

    @validator('color')
    def validate_color(cls, value):
        color = Color.objects.get(id=value)
        return color

    @validator('type')
    def validate_color(cls, value):
        types = Type.objects.get(id=value)
        return types


class ProductCreateUpdateResponse(BaseModel):
    """
    schema for product create or update response
    """
    id: str
    name: str
    price: float
    description: str
    image: str
    category: dict
    status: bool
    size: dict | None
    color: dict | None
    type: dict | None
