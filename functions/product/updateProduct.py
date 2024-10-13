import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products, ProductVariant
from schema.product import ProductCreateUpdateResponse, ProductUpdate
from utils.response import respond_success
from utils.exception_decorator import error_handler
from utils.middleware import update_product, vendors_login
from utils import helpers
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
@vendors_login
def main(event: LambdaContext, context: LambdaContext, **kwargs):
    path = event.get("path")

    if "/update/product" in path:
        return update_product(event=event, context=context, model=Products, vendor=kwargs['vendor'])
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


@update_product
def update_product(event: LambdaContext, context: LambdaContext, **kwargs):
    input_data = helpers.load_json(event=event)
    product = kwargs["product"]

    product_data = ProductUpdate(**input_data)

    for key, value in product_data.dict(exclude_none=True).items():
        setattr(product, key, [ProductVariant(**variant) if isinstance(variant, dict)
                else variant for variant in value] if key == 'variants' and value else value)
    product.save()

    response_data = ProductCreateUpdateResponse(
        id=str(product.id),
        name=product.name,
        description=product.description,
        image=product.image,
        price=product.price,
        category=product.category.to_dict(),
        status=product.status,
        type=product.type.to_dict(),
        variants=[data.to_dict() for data in product.variants],
        total_stock=product.total_stock
    )

    return respond_success(
        message='Product updated successfully',
        data=response_data.dict(),
        status_code=200,
        success=True
    )
