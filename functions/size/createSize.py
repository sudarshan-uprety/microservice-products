import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.size import Size
from models.admins import Admin
from schema.size import SizeCreate, SizeCreateUpdateResponse
from utils.database import db_config
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import helpers, response, constant
from utils.middleware import admin_login
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
@admin_login
def main(event: LambdaContext, context: LambdaContext, admin: Admin):
    path = event.get("path")

    if path == "/create/size":
        return create_size(event, context, admin)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def create_size(event: LambdaContext, context: LambdaContext, admin: Admin):
    input_data = helpers.load_json(event=event)

    # injecting admin to category
    input_data["created_by"] = admin.id

    # validate incoming data
    size_detail = SizeCreate(**input_data)

    # Create and save the product
    size = Size(**size_detail.dict())
    size.save()

    response_data = SizeCreateUpdateResponse(
        id=str(size.id),
        name=size_detail.name,
        description=size_detail.description,
        status=size_detail.status
    )

    # Return success response
    return response.success_response(
        status_code=201,
        message='Successfully created size',
        data=response_data.dict(),
        warning=None
    )
