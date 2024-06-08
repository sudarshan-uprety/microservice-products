from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)
import json


def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if "/update/product" in path:
        return update_product(event, context)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


def update_product(event: LambdaContext, context: LambdaContext):
    product_id = event.get("pathParameters", {}).get("id")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "product updated"})
    }
