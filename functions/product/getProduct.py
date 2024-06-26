import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayProxyEventV2,
)
from mongoengine import Q

from utils.database import db_config
from models.products import Products
from models.vendors import Vendors
from utils.exception_decorator import error_handler
from utils.response import respond_success
from utils import constant, object_fetch, pagination, helpers


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
    # pagination
    limit, skip, current_page = pagination.pagination(event=event)

    # call the db
    db_config()

    # first get the active vendors
    active_vendors = Vendors.objects.filter(is_active=True, is_deleted=False).values_list('id')

    products = Products.objects.filter(
        Q(status=True) &
        Q(is_deleted=False) &
        Q(vendor__in=active_vendors)
    ).limit(limit).skip(skip)

    product_response = object_fetch.product_fetch(products=products)

    return respond_success(
        data=product_response,
        success=True,
        message='Products retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None,
        total_page=products.count()/10,
        current_page=current_page
    )


def get_product_by_id(event: APIGatewayProxyEventV2, context: LambdaContext):
    product_id = event.get("pathParameters", {}).get("id")

    db_config()

    product = Products.objects.get(id=product_id)

    product_response = object_fetch.product_fetch(products=product)

    return respond_success(
        data=product_response,
        success=True,
        message='Product retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None
    )


def get_my_products(event: APIGatewayProxyEventV2, context: LambdaContext):
    # pagination
    limit, skip, current_page = pagination.pagination(event=event)

    # call the db
    db_config()

    # fetch vendor id from the lambda event
    vendor = helpers.vendor_check(vendor_sub=event['requestContext']['authorizer']['claims']['sub'])

    products = Products.objects.filter(
        vendor=vendor, is_deleted=False
    ).limit(limit).skip(skip)

    products_response = object_fetch.product_fetch(products=products)

    return respond_success(
        data=products_response,
        success=True,
        message='Products retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None,
        total_page=products.count() / 10,
        current_page=current_page
    )
