from pydantic import BaseModel


class CreateType(BaseModel):
    """schema for product model"""
    name: str
    description: str


class CreateUpdateTypeResponse(BaseModel):
    id: str
    name: str
    description: str


class UpdateType(BaseModel):
    name: str
    description: str


class GetTypeResponse(BaseModel):
    id: str
    name: str
    description: str
