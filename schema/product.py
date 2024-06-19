from typing import Optional, Dict

from pydantic import BaseModel, Field, field_validator, validator

from models.category import Category
from models.color import Color
from models.size import Size
from models.type import Type
from models.vendors import Vendors


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
    vendor: str
    type: str

    @field_validator('category')
    def validate_category(cls, value):
        category = Category.objects.get(id=value)
        return category

    @field_validator('size')
    def validate_size(cls, value):
        size = Size.objects.get(id=value)
        return size

    @field_validator('color')
    def validate_color(cls, value):
        color = Color.objects.get(id=value)
        return color

    @field_validator('type')
    def validate_type(cls, value):
        types = Type.objects.get(id=value)
        return types

    @field_validator('vendor')
    def validate_vendor(cls, value):
        vendor = Vendors.objects.get(id=value)
        return vendor


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


class GetProductResponse(BaseModel):
    """schema for get product model"""
    name: str
    price: float
    description: str
    image: str
    category: Optional[Dict]
    stock: int
    status: bool
    size: Optional[Dict] = Field(default=None)
    color: Optional[Dict] = Field(default=None)
    vendor: Optional[Dict]
    type: Optional[Dict]

    @field_validator('category')
    def validate_category(cls, value):
        if value is not None:
            category = Category.objects(id=value).first()
            if category:
                return {
                    'id': str(category.id),
                    'name': category.name
                }
        return {}

    @field_validator('size')
    def validate_size(cls, value):
        if value is not None:
            size = Size.objects(id=value).first()
            if size:
                return {
                    'id': str(size.id),
                    'name': size.name
                }
        return {}

    @field_validator('color')
    def validate_color(cls, value):
        if value is not None:
            color = Color.objects(id=value).first()
            if color:
                return {
                    'id': str(color.id),
                    'hex': color.hex
                }
        return {}

    @field_validator('type')
    def validate_type(cls, value):
        if value is not None:
            types = Type.objects(id=value).first()
            if types:
                return {
                    'id': str(types.id),
                    'name': types.name
                }
        return {}

    @field_validator('vendor')
    def validate_vendor(cls, value):
        if value is not None:
            vendor = Vendors.objects(id=value).first()
            if vendor:
                return {
                    'id': str(vendor.id),
                    'name': vendor.name
                }
        return {}
