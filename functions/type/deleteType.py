from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.type import Type
from models.admins import Admin
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant
from utils.middleware import admin_login, update_element
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
@admin_login
def main(event: LambdaContext, context: LambdaContext, admin: Admin):
    path = event.get("path")

    if "/delete/type/" in path:
        return delete_type(event, context, user=admin, model=Type)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


@update_element
def delete_type(event: LambdaContext, context: LambdaContext, **kwargs):
    obj = kwargs.get('element')
    obj.is_deleted = True
    obj.save()

    return respond_success(
        data=None,
        success=True,
        status_code=constant.SUCCESS_DELETED,
        message="Type deleted successfully.",
        warning=None
    )
