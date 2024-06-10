from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.color import Color
from utils.database import db_config
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, get_obj


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if "/delete/color/" in path:
        return delete_color(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def delete_color(event: LambdaContext, context: LambdaContext):
    color_id = event.get("pathParameters", {}).get("id")

    db_config()

    obj = get_obj.get_obj_or_404(Color, id=color_id)
    obj.is_deleted = True
    obj.save()

    return respond_success(
        status_code=200,
        data=None,
        success=True,
        message="Color deleted successfully",
        warning=None
    )

