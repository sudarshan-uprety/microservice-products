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

    if path == "/type/update":
        return update_type(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def update_type(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    update_data = UpdateType(**input_data)

    db_config()

    obj = get_obj.get_obj_or_404(model=Type, id=update_data.id)
    obj.name = update_data.name
    obj.description = update_data.description
    obj.status = update_data.status
    obj.save()

    return respond_success(
        data=update_data.dict(),
        success=True,
        status_code=constant.SUCCESS_UPDATED,
        message="Type updated.",
        warning=None
    )
