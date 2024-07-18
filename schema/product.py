from typing import Optional, Dict

from pydantic import BaseModel, Field, field_validator, model_validator, root_validator

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


class ProductUpdate(BaseModel):
    """schema for update product model"""
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    status: Optional[bool] = None
    size: Optional[str] = None
    color: Optional[str] = None
    vendor: Optional[str] = None
    type: Optional[str] = None

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
    id: str
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

    @model_validator(mode='before')
    def validate_references(cls, values):
        def get_reference_dict(ref, model, fields):
            if ref is not None:
                obj = model.objects(id=ref).first()
                if obj:
                    return {field: str(getattr(obj, field)) for field in fields}
            return None

        values['category'] = get_reference_dict(values.get('category'), Category, ['id', 'name', 'description'])
        values['size'] = get_reference_dict(values.get('size'), Size, ['id', 'name', 'description'])
        values['color'] = get_reference_dict(values.get('color'), Color, ['id', 'hex'])
        values['type'] = get_reference_dict(values.get('type'), Type, ['id', 'name', 'description'])
        values['vendor'] = get_reference_dict(values.get('vendor'), Vendors, ['id', 'store_name'])

        return values
