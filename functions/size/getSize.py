from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)


from utils.database import db_config
from models.size import Size
from schema.size import GetSizeResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant


@error_handler
def main(event: APIGatewayProxyEventV2, context: LambdaContext):
    path = event.get("path")

    if path == "/get/sizes":
        return get_all_size(event, context)

    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def get_all_size(event: APIGatewayProxyEventV2, context: LambdaContext):
    db_config()

    size = Size.objects.filter(status=True, is_deleted=False)

    size_responses = [
        GetSizeResponse(
            id=str(size.id),
            name=size.name,
            description=size.description,
            status=size.status,
        ).dict()
        for size in size
    ]

    return respond_success(
        data=size_responses,
        success=True,
        message='Size retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None
    )
