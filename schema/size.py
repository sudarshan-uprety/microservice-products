from pydantic import BaseModel


class SizeCreate(BaseModel):
    name: str
    description: str
    created_by: str


class SizeUpdate(BaseModel):
    name: str
    description: str


class SizeCreateUpdateResponse(BaseModel):
    id: str
    name: str
    description: str


class GetSizeResponse(BaseModel):
    id: str
    name: str
    description: str
