from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.color import Color
from models.admins import Admin
from utils.database import db_config
from schema.color import ColorUpdate, ColorCreateUpdateResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, get_obj
from utils.middleware import admin_login, update_element
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
@admin_login
def main(event: LambdaContext, context: LambdaContext, admin: Admin):
    path = event.get("path")

    if "/update/color/" in path:
        return update_color(event, context, user=admin, model=Color)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


@update_element
def update_color(event: LambdaContext, context: LambdaContext, **kwargs):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    update_data = ColorUpdate(**input_data)

    db_config()

    obj = kwargs.get('element')
    obj.name = update_data.name
    obj.hex = update_data.hex
    obj.status = update_data.status
    obj.save()

    # response data
    response_data = ColorCreateUpdateResponse(**obj.to_dict())

    return respond_success(
        data=response_data.dict(),
        success=True,
        status_code=constant.SUCCESS_UPDATED,
        message="Color updated.",
        warning=None
    )
