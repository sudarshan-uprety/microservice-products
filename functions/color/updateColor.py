from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.color import Color
from utils.database import db_config
from schema.color import ColorUpdate, ColorCreateUpdateResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, get_obj


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if "/update/color/" in path:
        return update_color(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def update_color(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)
    color_id = event.get("pathParameters", {}).get("id")

    # validate incoming data
    update_data = ColorUpdate(**input_data)

    db_config()

    obj = get_obj.get_obj_or_404(model=Color, id=color_id)
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
