from pydantic import BaseModel


class CreateColor(BaseModel):
    """schema for product model"""
    name: str
    hex: str
    created_by: str


class ColorUpdate(BaseModel):
    name: str
    hex: str


class ColorCreateUpdateResponse(BaseModel):
    id: str
    name: str
    hex: str


class GetColorResponse(BaseModel):
    id: str
    name: str
    hex: str
