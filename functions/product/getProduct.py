import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)


from utils.database import db_config
from models.products import Products
from utils.exception_decorator import error_handler


@error_handler
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
    # call the db
    db_config()

    products = Products.objects.exclude('created_at', 'updated_at').to_json()
    products_json = json.loads(products)

    return {
        "statusCode": 200,
        "body": json.dumps({"data": products_json})
    }


def get_product_by_id(event: APIGatewayProxyEventV2, context: LambdaContext):
    product_id = event.get("pathParameters", {}).get("id")

    db_config()

    product = Products.objects.get(id=product_id).to_json()
    products_json = json.loads(product)

    return {
        "statusCode": 200,
        "body": json.dumps({"data": products_json})
    }


def get_my_products(event: APIGatewayProxyEventV2, context: LambdaContext):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Fetched my products"})
    }
