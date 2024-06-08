from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.type import Type
from utils.database import db_config
from schema.type import CreateType, CreateUpdateTypeResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/create/type":
        return create_type(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def create_type(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    db_config()

    # validation for incoming product data.
    type_data = CreateType(**input_data)

    # Create Type obj and save
    types = Type(**type_data.dict())
    types.save()

    size_response = CreateUpdateTypeResponse(
        id=str(types.id),
        name=types.name,
        description=types.description,
        status=types.status,
    )

    # Return success response
    return respond_success(
        data=size_response.dict(),
        success=True,
        status_code=constant.SUCCESS_CREATED,
        message="Type created.",
        warning=None
    )
