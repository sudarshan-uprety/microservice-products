import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from utils.database import db_config
from utils.get_obj import get_obj_or_404
from utils.response import respond_success, respond_error
from utils import helpers, constant


def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if "/delete/product" in path:
        return delete_product(event, context)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


def delete_product(event: LambdaContext, context: LambdaContext):
    product_id = event.get("pathParameters", {}).get("id")

    db_config()

    # fetch vendor id from the lambda event
    vendor = helpers.vendor_check(vendor_sub=event['requestContext']['authorizer']['claims']['sub'])

    obj = get_obj_or_404(Products, id=product_id)

    if obj.vendor.id == vendor.id:
        obj.is_deleted = True
        obj.save()

        return respond_success(
            status_code=200,
            data=None,
            success=True,
            message="Color deleted successfully",
            warning=None
        )
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            data=None,
            success=False,
            message="Current vendor is not the owner of the product."
        )

