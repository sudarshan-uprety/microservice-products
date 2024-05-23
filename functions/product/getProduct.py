from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)
import json


def main(event: APIGatewayProxyEventV2, context: LambdaContext):
    path = event.get("path")

    if path == "/get/products":
        return get_all_products(event, context)

    elif "/get/product/" in path:
        return get_product_by_id(event, context)

    elif path == "/get/my/products":
        return get_my_products(event, context)

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


def get_all_products(event: APIGatewayProxyEventV2, context: LambdaContext):
    print("Fetching all products")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Fetched all products"})
    }


def get_product_by_id(event: APIGatewayProxyEventV2, context: LambdaContext):
    product_id = event.get("pathParameters", {}).get("id")
    print(f"Fetching product with ID: {product_id}")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Fetched product with ID: {product_id}"})
    }


def get_my_products(event: APIGatewayProxyEventV2, context: LambdaContext):
    print("Fetching my products")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Fetched my products"})
    }
