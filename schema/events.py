from typing import List, Optional

from pydantic import BaseModel, field_validator

from models.products import Products


class ProductsDetails(BaseModel):
    product_id: str
    size: Optional[str] = None
    color: Optional[str] = None
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

            variant = next((v for v in db_product.variants if
                            v['size'] == product_detail.size and v['color'] == product_detail.color), None)
            if not variant:
                raise ValueError(
                    f"Variant with size {product_detail.size} and color {product_detail.color} not found for product {product_detail.product_id}.")

            if variant['stock'] < product_detail.quantity:
                raise ValueError(
                    f"Insufficient stock for variant (size: {variant['size']}, color: {variant['color']}) of product {db_product.id}")

            validated_products.append({
                'product': db_product,
                'variant': variant,
                'quantity': product_detail.quantity
            })
        return validated_products
