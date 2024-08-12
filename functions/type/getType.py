from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)

from utils import pagination, object_fetch


from utils.database import db_config
from models.type import Type
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
def main(event: APIGatewayProxyEventV2, context: LambdaContext):
    path = event.get("path")

    if path == "/get/types":
        return get_all_type(event, context)

    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def get_all_type(event: APIGatewayProxyEventV2, context: LambdaContext):
    # pagination
    limit, skip, current_page = pagination.pagination(event=event)

    # call the db
    db_config()

    # fetch type objects
    types = Type.objects.filter(status=True, is_deleted=False).limit(limit).skip(skip)

    # response
    type_responses = object_fetch.type_fetch(types)

    return respond_success(
        data=type_responses,
        success=True,
        message='Size retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None,
        total_page=types.count()/10,
        current_page=current_page
    )
