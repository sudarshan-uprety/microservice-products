import json
from datetime import datetime

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from pydantic import ValidationError

from models.size import Size
from schema.size import SizeCreate
from utils.database import db_config


def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/create/size":
        return create_size(event, context)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


def create_size(event: LambdaContext, context: LambdaContext):
    try:
        size_details = json.loads(event['body'])
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Empty body"})
        }

    try:
        size_input = SizeCreate(**size_details)
    except ValidationError as e:
        error_dict = {}
        for error in e.errors():
            field = error['loc'][-1]
            message = error['msg']
            error_dict[field] = message

        return {
            "statusCode": 400,
            "body": json.dumps({"error": error_dict})
        }

    # Add timestamps
    size_details['created_at'] = datetime.utcnow()
    size_details['updated_at'] = datetime.utcnow()

    db_config()

    # Create and save the product
    size = Size(**size_details)
    size.save()

    # Return success response
    return {
        "statusCode": 201,
        "body": json.dumps({"message": "size created", "details": {'size_name': size.name}})
    }
