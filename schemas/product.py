from pydantic import BaseModel


class CreateProduct(BaseModel):
    name = str
    price = float
    description = str
    image = str
    category = str
    stock = int
    status = bool
    vendor = str