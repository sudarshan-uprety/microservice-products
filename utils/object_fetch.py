from mongoengine import QuerySet

from schema.product import GetProductResponse
from schema.type import GetTypeResponse
from schema.color import GetColorResponse
from schema.category import GetCategoryResponse
from schema.size import GetSizeResponse


def fetch_all_products(products):
    if not isinstance(products, (list, QuerySet)):
        products = [products]
    product_responses = [
        GetProductResponse(
            id=str(product.id),
            name=product.name,
            price=product.price,
            description=product.description,
            image=product.image,
            category=product.category.id if product.category else None,
            stock=product.stock,
            status=product.status,
            size=product.size.id if product.size else None,
            color=product.color.id if product.color else None,
            type=product.type.id if product.type else None,
            vendor=product.vendor.id if product.vendor else None
        ).dict()
        for product in products
    ]
    return product_responses


def fetch_product(product):
    print(product)
    product = GetProductResponse(
        id=str(product.id),
        name=product.name,
        price=product.price,
        description=product.description,
        image=product.image,
        category=product.category.id if product.category else None,
        stock=product.stock,
        status=product.status,
        size=product.size.id if product.size else None,
        color=product.color.id if product.color else None,
        type=product.type.id if product.type else None,
        vendor=product.vendor.id if product.vendor else None
    ).dict()
    return product


def type_fetch(types):
    if not isinstance(types, (list, QuerySet)):
        types = [types]

    type_responses = [
        GetTypeResponse(
            id=str(types.id),
            name=types.name,
            description=types.description,
            status=types.status,
        ).dict()
        for types in types
    ]
    return type_responses


def color_fetch(colors):
    if not isinstance(colors, (list, QuerySet)):
        types = [colors]

    color_responses = [
        GetColorResponse(
            id=str(color.id),
            name=color.name,
            hex=color.hex,
            status=color.status,
        ).dict()
        for color in colors
    ]
    return color_responses


def category_fetch(categories):
    if not isinstance(categories, (list, QuerySet)):
        categories = [categories]

    category_responses = [
        GetCategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description,
            status=category.status,
        ).dict()
        for category in categories
    ]
    return category_responses


def size_fetch(sizes):
    if not isinstance(sizes, (list, QuerySet)):
        categories = [sizes]

    size_responses = [
        GetSizeResponse(
            id=str(size.id),
            name=size.name,
            description=size.description,
            status=size.status,
        ).dict()
        for size in sizes
    ]
    return size_responses
