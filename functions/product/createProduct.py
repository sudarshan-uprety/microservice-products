from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)
import json


def handler(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/create/product":
        return create_product(event, context)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


def create_product(event: LambdaContext, context: LambdaContext):
    # create a product
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "product created"})
    }