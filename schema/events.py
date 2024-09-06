from typing import List

from pydantic import BaseModel, field_validator

from models.products import Products


class ProductsDetails(BaseModel):
    product_id: str
    quantity: int


class Event(BaseModel):
    event_name: str
    products: List[ProductsDetails]

    @field_validator('products')
    def validate_products(cls, value):
        validated_products = []
        for product_detail in value:
            db_product = Products.objects.filter(id=product_detail.product_id, status=True, is_deleted=False).first()
            if not db_product:
                raise ValueError(f"Product with ID {product_detail.product_id} not found or inactive.")
            validated_products.append({
                'product': db_product,
                'quantity': product_detail.quantity
            })
        return validated_products
