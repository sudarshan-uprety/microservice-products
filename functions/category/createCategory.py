from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.category import Category
from utils.database import db_config
from schema.category import CategoryCreate, CategoryCreateUpdateResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/create/category":
        return create_category(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def create_category(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    db_config()

    # validation for incoming data.
    category_data = CategoryCreate(**input_data)

    # Create category obj and save
    category = Category(**category_data.dict())
    category.save()

    category_response = CategoryCreateUpdateResponse(
        id=str(category.id),
        name=category.name,
        description=category.description,
        status=category.status,
    )

    # Return success response
    return respond_success(
        data=category_response.dict(),
        success=True,
        status_code=constant.SUCCESS_CREATED,
        message="Category created.",
        warning=None
    )
