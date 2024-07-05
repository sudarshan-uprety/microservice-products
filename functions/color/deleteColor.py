from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.color import Color
from models.admins import Admin
from utils.database import db_config
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, get_obj
from utils.middleware import admin_login, update_element


@error_handler
@admin_login
def main(event: LambdaContext, context: LambdaContext, admin: Admin):
    path = event.get("path")

    if "/delete/color/" in path:
        return delete_color(event, context, user=admin, model=Color)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


@update_element
def delete_color(event: LambdaContext, context: LambdaContext, **kwargs):
    obj = kwargs.get("element")
    obj.is_deleted = True
    obj.save()

    return respond_success(
        status_code=200,
        data=None,
        success=True,
        message="Color deleted successfully",
        warning=None
    )

