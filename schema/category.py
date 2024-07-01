from pydantic import BaseModel, validator


class CategoryCreate(BaseModel):
    """schema for product model"""
    name: str
    description: str
    status: bool


class CategoryUpdate(BaseModel):
    """schema for updating category"""
    name: str
    description: str
    status: bool


class CategoryCreateUpdateResponse(BaseModel):
    id: str
    name: str
    description: str
    status: bool


class GetCategoryResponse(BaseModel):
    id: str
    name: str
    description: str
    status: bool
