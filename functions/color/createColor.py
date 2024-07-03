from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.color import Color
from models.admins import Admin
from utils.database import db_config
from schema.color import CreateColor, ColorCreateUpdateResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers
from utils.middleware import admin_login


@error_handler
@admin_login
def main(event: LambdaContext, context: LambdaContext, admin: Admin):
    path = event.get("path")

    if path == "/create/color":
        return create_color(event, context, admin)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def create_color(event: LambdaContext, context: LambdaContext, admin: Admin):
    input_data = helpers.load_json(event=event)

    # injecting created by user
    input_data["created_by"] = admin.id

    # validation for incoming data.
    color_data = CreateColor(**input_data)

    # Create color obj and save
    color = Color(**color_data.dict())
    color.save()

    color_response = ColorCreateUpdateResponse(
        id=str(color.id),
        name=color.name,
        hex=color.hex,
        status=color.status,
    )

    # Return success response
    return respond_success(
        data=color_response.dict(),
        success=True,
        status_code=constant.SUCCESS_CREATED,
        message="Color created.",
        warning=None
    )
