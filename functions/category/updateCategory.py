from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.category import Category
from utils.database import db_config
from schema.category import CategoryCreateUpdateResponse, CategoryUpdate
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, get_obj


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if "/update/category/" in path:
        return update_category(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def update_category(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)
    category_id = event.get("pathParameters", {}).get("id")

    # validate incoming data
    update_data = CategoryUpdate(**input_data)

    db_config()

    obj = get_obj.get_obj_or_404(model=Category, id=category_id)
    obj.name = update_data.name
    obj.description = update_data.description
    obj.status = update_data.status
    obj.save()

    # response data
    response_data = CategoryCreateUpdateResponse(**obj.to_dict())

    return respond_success(
        data=response_data.dict(),
        success=True,
        status_code=constant.SUCCESS_UPDATED,
        message="Category updated.",
        warning=None
    )
