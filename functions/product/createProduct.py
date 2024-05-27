import json
from datetime import datetime

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
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
        "statusCode": 201,
        "body": json.dumps({"message": "product created"})
    }
