from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.color import Color
from utils.database import db_config
from schema.color import CreateColor, ColorCreateUpdateResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/create/color":
        return create_color(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def create_color(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    db_config()

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
