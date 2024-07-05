from pydantic import BaseModel


class SizeCreate(BaseModel):
    name: str
    description: str
    status: bool
    created_by: str


class SizeUpdate(BaseModel):
    name: str
    description: str
    status: bool


class SizeCreateUpdateResponse(BaseModel):
    id: str
    name: str
    description: str
    status: bool


class GetSizeResponse(BaseModel):
    id: str
    name: str
    description: str
    status: bool
