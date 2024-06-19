from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)


from utils.database import db_config
from models.category import Category
from schema.category import GetCategoryResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers


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
    db_config()

    category = Category.objects.filter(status=True, is_deleted=False)

    category_responses = [
        GetCategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description,
            status=category.status,
        ).dict()
        for category in category
    ]

    return respond_success(
        data=category_responses,
        success=True,
        message='Categories retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None
    )
