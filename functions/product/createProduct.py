import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from utils.database import db_config
from schema.product import ProductCreate
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/create/product":
        return create_product(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def create_product(event: LambdaContext, context: LambdaContext):
    body = event.get('body')

    if not body:
        return respond_error(
            status_code=400,
            message="Missing body",
            data=None,
            success=False
        )

    product_details = json.loads(body)

    db_config()

    # validation for incoming product data.
    input_data = ProductCreate(**product_details)

    # Create product obj and save
    product = Products(**input_data.dict())
    product.save()

    # response data
    response_data = input_data.dict(exclude={'category'})

    # Return success response
    return respond_success(
        status_code=constant.SUCCESS_CREATED,
        success=True,
        data=response_data,
        warning=None,
        message="Product created",
    )
