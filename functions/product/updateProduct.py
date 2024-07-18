import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from schema.product import ProductCreateUpdateResponse, ProductUpdate
from utils.response import respond_success
from utils.exception_decorator import error_handler
from utils.middleware import update_product, vendors_login
from utils import helpers


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
        setattr(product, key, value)
    product.save()

    response_data = ProductCreateUpdateResponse(
        id=str(product.id),
        name=product.name,
        description=product.description,
        image=product.image,
        price=product.price,
        category=product.category.to_dict(),
        status=product.status,
        size=product.size.to_dict() if product.size else None,
        color=product.color.to_dict() if product.color else None,
        type=product.type.to_dict(),
    )

    return respond_success(
        message='Product updated successfully',
        data=response_data.dict(),
        status_code=200,
        success=True
    )
