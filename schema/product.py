from typing import Optional, Dict, List, Union

from pydantic import BaseModel, Field, field_validator, model_validator, root_validator

from models.category import Category
from models.color import Color
from models.size import Size
from models.type import Type
from models.vendors import Vendors


class VariantCreate(BaseModel):
    size: Optional[str] = None
    color: Optional[str] = None
    stock: int

    @property
    def total_stock(self):
        return self.stock


class ProductCreate(BaseModel):
    """schema for product model"""
    name: str
    price: float
    description: str
    image: List[str]
    category: str
    status: bool
    vendor: str
    type: str
    variants: List[VariantCreate]

    @property
    def total_stock(self) -> int:
        return sum(variant.stock for variant in self.variants)

    @field_validator('category')
    def validate_category(cls, value):
        category = Category.objects.get(id=value)
        return category

    @field_validator('type')
    def validate_type(cls, value):
        types = Type.objects.get(id=value)
        return types

    @field_validator('vendor')
    def validate_vendor(cls, value):
        vendor = Vendors.objects.get(id=value)
        return vendor


class VariantResponse(BaseModel):
    size: Optional[dict] = None
    color: Optional[dict] = None
    stock: int


class ProductUpdate(BaseModel):
    """schema for update product model"""
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[List[str]] = None
    category: Optional[str] = None
    status: Optional[bool] = None
    vendor: Optional[str] = None
    type: Optional[str] = None
    variants: Optional[List[VariantCreate]] = None

    @field_validator('category')
    def validate_category(cls, value):
        category = Category.objects.get(id=value)
        return category

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
    image: List[str]
    category: dict
    status: bool
    type: dict | None
    total_stock: int
    variants: List[dict]


class GetProductResponse(BaseModel):
    """schema for get product model"""
    id: str
    name: str
    price: float
    description: str
    image: List[str]
    category: Optional[Dict]
    status: bool
    vendor: Optional[Dict]
    type: Optional[Dict]
    total_stock: int
    variants: List[dict]

    @model_validator(mode='before')
    def validate_references(cls, values):
        def get_reference_dict(ref, model, fields):
            if ref is not None:
                obj = model.objects(id=ref).first()
                if obj:
                    return {field: str(getattr(obj, field)) for field in fields}
            return None

        values['category'] = get_reference_dict(values.get('category'), Category, ['id', 'name', 'description'])
        values['type'] = get_reference_dict(values.get('type'), Type, ['id', 'name', 'description'])
        values['vendor'] = get_reference_dict(values.get('vendor'), Vendors, ['id', 'store_name'])

        return values
