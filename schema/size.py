from pydantic import BaseModel


class SizeCreate(BaseModel):
    name: str
    description: str
    status: bool


class SizeCreateUpdateResponse(BaseModel):
    id: str
    name: str
    description: str
    status: bool
