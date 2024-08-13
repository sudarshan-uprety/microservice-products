from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.size import Size
from models.admins import Admin
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils.middleware import admin_login
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
@admin_login
def main(event: LambdaContext, context: LambdaContext, admin: Admin):
    path = event.get("path")

    if "/delete/size/" in path:
        return delete_size(event, context, user=admin, model=Size)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def delete_size(event: LambdaContext, context: LambdaContext, **kwargs):
    obj = kwargs.get('element')
    obj.is_deleted = True
    obj.save()

    return respond_success(
        status_code=200,
        data=None,
        success=True,
        message="Size deleted successfully",
        warning=None
    )

