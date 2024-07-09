import base64
import json
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from utils.database import db_config
from schema.product import ProductCreate, ProductCreateUpdateResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, decrypt_payload, s3


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
    input_data, image = decrypt_payload.decrypt_payload(event=event)

    db_config()

    # check if vendor is active or not
    vendor = helpers.vendor_check(
        vendor_sub=event['requestContext']['authorizer']['claims']['sub']
    )

    validation_data = input_data.copy()
    validation_data['vendor'] = str(vendor.id)
    validation_data['image'] = "placeholder_for_validation"

    # validation for incoming data.
    product_details = ProductCreate(**validation_data)

    image_url = s3.upload_image(image)

    product_details.image = image_url

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
        size=product.size.to_dict() if product.size else None,
        color=product.color.to_dict() if product.color else None,
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
