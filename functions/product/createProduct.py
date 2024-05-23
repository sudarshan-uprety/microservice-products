import json
from datetime import datetime

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)
from aws_lambda_powertools.utilities.parser import event_parser, parse, BaseModel, envelopes

from models.products import Products
from schemas.createProduct import CreateProduct
from utils.database import db_config


def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/create/product":
        return create_product(event, context)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


@event_parser(model=CreateProduct, envelopes=envelopes.EventBridgeEnvelope)
def create_product(event: LambdaContext, context: LambdaContext):
    product_details = json.loads(event['body'])

    # Add timestamps
    product_details['created_at'] = datetime.utcnow()
    product_details['updated_at'] = datetime.utcnow()

    db_config()

    # Create and save the product
    product = Products(**product_details)
    product.save()

    # Return success response
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "product created"})
    }