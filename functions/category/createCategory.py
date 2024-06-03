import json
from datetime import datetime

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.category import Category
from utils.database import db_config
from schema.category import CategoryCreate
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant


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
    body = event.get('body')

    if not body:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Missing body",
            data=None,
            success=False
        )

    category_details = json.loads(body)

    # Add timestamps
    category_details['created_at'] = datetime.utcnow()
    category_details['updated_at'] = datetime.utcnow()

    db_config()

    # validation for incoming product data.
    input_data = CategoryCreate(**category_details)

    # Create and save the category
    product = Category(**input_data.dict())
    product.save()

    # Return success response
    return respond_success(
        data=input_data.dict(),
        success=True,
        status_code=constant.SUCCESS_CREATED,
        message="Category created.", warning=None
    )
