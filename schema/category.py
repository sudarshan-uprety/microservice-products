from pydantic import BaseModel, field_validator

from models.admins import Admin


class CategoryCreate(BaseModel):
    """schema for product model"""
    name: str
    description: str
    created_by: str


class CategoryUpdate(BaseModel):
    """schema for updating category"""
    name: str
    description: str


class CategoryCreateUpdateResponse(BaseModel):
    id: str
    name: str
    description: str


class GetCategoryResponse(BaseModel):
    id: str
    name: str
    description: str
