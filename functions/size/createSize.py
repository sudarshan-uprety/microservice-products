import json
from datetime import datetime

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from pydantic import ValidationError

from models.size import Size
from schema.size import SizeCreate, SizeCreateUpdateResponse
from utils.database import db_config
from utils.exception_decorator import error_handler
from utils import helpers, response


@error_handler
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
    input_data = helpers.load_json(event=event)

    # validate incoming data
    size_detail = SizeCreate(**input_data)

    db_config()

    # Create and save the product
    size = Size(**size_detail.dict())
    size.save()

    response_data = SizeCreateUpdateResponse(
        id=str(size.id),
        name=size_detail.name,
        description=size_detail.description,
        status=size_detail.status
    )

    # Return success response
    return response.success_response(
        status_code=201,
        message='Successfully created size',
        data=response_data.dict(),
        warning=None
    )
