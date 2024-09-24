from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from schema.events import Event
from utils.database import db_config
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, variables
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/consume/event":
        return event_handler(event, context)

    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def event_handler(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # calling the database function
    db_config()
    data = Event(**input_data)

    if data.event_name == variables.DECREASE_PRODUCT_QUANTITY_EVENT:
        response = product_decrease_handler(data=data)
    elif data.event_name == variables.INCREASE_PRODUCT_QUANTITY_EVENT:
        response = product_increase_handler(product=product, quantity=quantity)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid operation",
            data=None,
            success=False
        )
    return response


def product_decrease_handler(data: Event) -> bool:
    for product in data.products:
        product_obj = product['product']
        product_obj.total_stock -= product['quantity']
        product_obj.save()
    return respond_success(
        status_code=constant.SUCCESS_UPDATED,
        success=True,
        data=None,
        warning=None,
        message="Product decreased.",
    )


def product_increase_handler(product: Products, quantity: int) -> bool:
    product.stock += quantity
    product.save()
    return respond_success(
        status_code=constant.SUCCESS_UPDATED,
        success=True,
        data=None,
        warning=None,
        message="Product increased.",
    )
