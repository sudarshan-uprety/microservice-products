from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from utils.database import db_config
from schema.product import ProductCreate, ProductCreateUpdateResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, decrypt_payload, s3
from utils.middleware import vendors_login
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
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


@vendors_login
def create_product(event: LambdaContext, context: LambdaContext, **kwargs):
    input_data = helpers.load_json(event=event)

    db_config()
    input_data['vendor'] = str(kwargs['vendor'].id)

    # validation for incoming data.
    product_details = ProductCreate(**input_data)

    # Create product obj and save
    product = Products(**product_details.dict())
    product.save()

    # response data
    response_data = ProductCreateUpdateResponse(
        id=str(product.id),
        name=product.name,
        description=product.description,
        image=product.image,
        price=product.price,
        category=product.category.to_dict(),
        status=product.status,
        size=[size.to_dict() for size in product.size] if product.size else None,
        color=[color.to_dict() for color in product.color] if product.color else None,
        type=product.type.to_dict(),
    )

    # Return success response
    return respond_success(
        status_code=constant.SUCCESS_CREATED,
        success=True,
        data=response_data.dict(),
        warning=None,
        message="Product created",
    )
