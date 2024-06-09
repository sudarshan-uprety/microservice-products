from pydantic import BaseModel


class CreateType(BaseModel):
    """schema for product model"""
    name: str
    description: str
    status: bool


class CreateUpdateTypeResponse(BaseModel):
    id: str
    name: str
    description: str
    status: bool


class UpdateType(BaseModel):
    id: str
    name: str
    description: str
    status: bool
