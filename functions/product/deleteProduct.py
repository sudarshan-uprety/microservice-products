import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from utils.response import respond_success
from utils.exception_decorator import error_handler
from utils.middleware import vendors_login, update_product
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
@vendors_login
def main(event: LambdaContext, context: LambdaContext, **kwargs):
    path = event.get("path")

    if "/delete/product" in path:
        return delete_product(event=event, context=context, model=Products, vendor=kwargs['vendor'])
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


@update_product
def delete_product(event: LambdaContext, context: LambdaContext, **kwargs):
    product = kwargs["product"]

    product.is_deleted = True
    product.save()

    return respond_success(
        status_code=200,
        data=None,
        success=True,
        message="Product deleted successfully",
        warning=f"Product of id {product.id} was deleted"
    )
