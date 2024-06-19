from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)


from utils.database import db_config
from models.type import Type
from schema.type import GetTypeResponse
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant


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
    db_config()

    types = Type.objects.filter(status=True, is_deleted=False)

    type_responses = [
        GetTypeResponse(
            id=str(types.id),
            name=types.name,
            description=types.description,
            status=types.status,
        ).dict()
        for types in types
    ]

    return respond_success(
        data=type_responses,
        success=True,
        message='Size retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None
    )
