from pydantic import BaseModel, validator


class CategoryCreate(BaseModel):
    """schema for product model"""
    name: str
    description: str
    status: bool
