from pydantic import BaseModel


class CreateColor(BaseModel):
    """schema for product model"""
    name: str
    hex: str
    status: bool
    created_by: str


class ColorUpdate(BaseModel):
    name: str
    hex: str
    status: bool


class ColorCreateUpdateResponse(BaseModel):
    id: str
    name: str
    hex: str
    status: bool


class GetColorResponse(BaseModel):
    id: str
    name: str
    hex: str
    status: bool
