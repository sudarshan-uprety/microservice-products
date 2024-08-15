from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)

from utils.database import db_config
from models.category import Category
from schema.category import GetCategoryResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, object_fetch, pagination
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
def main(event: APIGatewayProxyEventV2, context: LambdaContext):
    path = event.get("path")

    if path == "/get/categories":
        return get_all_categories(event, context)

    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def get_all_categories(event: APIGatewayProxyEventV2, context: LambdaContext):
    # pagination
    limit, skip, current_page = pagination.pagination(event=event)

    # call the db
    db_config()

    # get category objects
    category = Category.objects.filter(status=True, is_deleted=False).limit(limit).skip(skip)

    category_responses = object_fetch.category_fetch(categories=category)

    return respond_success(
        data=category_responses,
        success=True,
        message='Categories retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None,
        current_page=current_page,
        total_page=category.count() / 10
    )
