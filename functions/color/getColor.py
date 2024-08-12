from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)

from utils.database import db_config
from models.color import Color
from schema.color import GetColorResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, helpers, pagination, object_fetch
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
def main(event: APIGatewayProxyEventV2, context: LambdaContext):
    path = event.get("path")

    if path == "/get/colors":
        return get_all_colors(event, context)

    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def get_all_colors(event: APIGatewayProxyEventV2, context: LambdaContext):
    # pagination
    limit, skip, current_page = pagination.pagination(event=event)

    # call the db
    db_config()

    # get the color objects
    colors = Color.objects.filter(status=True, is_deleted=False).skip(skip).limit(limit)

    color_responses = object_fetch.color_fetch(colors=colors)

    return respond_success(
        data=color_responses,
        success=True,
        message='Color retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None,
        total_page=colors.count()/10,
        current_page=current_page
    )
