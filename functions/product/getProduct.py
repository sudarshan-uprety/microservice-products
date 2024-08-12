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
from utils import constant, object_fetch, pagination
from utils.lambda_middleware import lambda_middleware
from utils.middleware import vendors_login, admin_login


@lambda_middleware
@error_handler
def main(event: APIGatewayProxyEventV2, context: LambdaContext):
    path = event.get("path")

    if path == "/get/products":
        return get_all_products(event, context)

    elif "/get/product/" in path:
        return get_product_by_id(event, context)

    elif path == "/get/my/products":
        return get_my_products(event, context)

    elif path == "/get/admin/products":
        return admin_products(event, context)

    elif "/get/vendor/product" in path:
        return vendor_product_details(event, context)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


def get_all_products(event: APIGatewayProxyEventV2, context: LambdaContext):
    # pagination and query filter
    limit, skip, current_page = pagination.pagination(event=event)
    db_config()
    query_filter = pagination.query_filter(event=event)

    base_query = Q(is_deleted=False, status=True)

    # first get the active vendors
    active_vendors = Vendors.objects.filter(is_active=True, is_deleted=False).values_list('id')

    products = Products.objects.filter(
        Q(vendor__in=active_vendors) &
        base_query &
        query_filter
    ).limit(limit).skip(skip)

    product_response = object_fetch.fetch_all_products(products=products)

    return respond_success(
        data=product_response,
        success=True,
        message='Products retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None,
        total_page=products.count() / 10,
        current_page=current_page
    )


def get_product_by_id(event: APIGatewayProxyEventV2, context: LambdaContext):
    product_id = event.get("pathParameters", {}).get("id")

    db_config()

    product = Products.objects.get(id=product_id, is_deleted=False, status=True)

    product_response = object_fetch.fetch_product(product=product)

    return respond_success(
        data=product_response,
        success=True,
        message='Product retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None
    )


@vendors_login
def get_my_products(event: APIGatewayProxyEventV2, context: LambdaContext, **kwargs):
    # pagination and query filter
    limit, skip, current_page = pagination.pagination(event=event)
    query_filter = pagination.query_filter(event=event)

    # fetch vendor id from the lambda event
    vendor = kwargs['vendor']

    base_query = Q(vendor=vendor, is_deleted=False)
    products = Products.objects(base_query & query_filter).limit(limit).skip(skip)

    products_response = object_fetch.fetch_all_products(products=products)

    return respond_success(
        data=products_response,
        success=True,
        message='Products retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None,
        total_page=products.count() / 10,
        current_page=current_page
    )


@admin_login
def admin_products(event: APIGatewayProxyEventV2, context: LambdaContext):
    # pagination and query filter
    limit, skip, current_page = pagination.pagination(event=event)
    query_filter = pagination.query_filter(event=event)

    base_query = Q(is_deleted=False, status=True)
    products = Products.objects.filter(base_query & query_filter).limit(limit).skip(skip)

    products_response = object_fetch.fetch_all_products(products=products)

    return respond_success(
        data=products_response,
        success=True,
        message='Products retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None
    )


@vendors_login
def vendor_product_details(event: APIGatewayProxyEventV2, context: LambdaContext, **kwargs):
    product_id = event.get("pathParameters", {}).get("id")

    product = Products.objects.get(id=product_id, is_deleted=False, vendor=kwargs['vendor'])
    product_response = object_fetch.fetch_product(product=product)

    return respond_success(
        data=product_response,
        success=True,
        message='Product retrieved',
        status_code=constant.SUCCESS_RESPONSE,
        warning=None
    )
