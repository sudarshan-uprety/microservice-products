from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.type import Type
from utils.database import db_config
from schema.type import CreateType, CreateUpdateTypeResponse, UpdateType
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, get_obj


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")
    if path == "/type/delete/":
        return delete_type(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def delete_type(event: LambdaContext, context: LambdaContext):
    product_id = event.get("pathParameters", {}).get("id")

    db_config()

    obj = get_obj.get_obj_or_404(model=Type, id=product_id)
    obj.status = False
    obj.save()

    return respond_success(
        data=None,
        success=True,
        status_code=constant.SUCCESS_DELETED,
        message="Type delete.",
        warning=None
    )
