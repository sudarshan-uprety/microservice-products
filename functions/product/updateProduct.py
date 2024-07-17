import json

from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from models.products import Products
from schema.product import ProductCreate, ProductCreateUpdateResponse
from utils.response import respond_success, respond_error
from utils import get_obj, s3
from utils.exception_decorator import error_handler
from utils.middleware import update_element


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if "/update/product" in path:
        return update_product(event, context, model=Products)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid path"})
        }


@update_element
def update_product(event: LambdaContext, context: LambdaContext, model: Products):

    product_obj = get_obj.get_obj_or_404(model=Products, id=product_id)
    if product_obj.vendor.id == vendor.id:

        validation_data = input_data.copy()
        validation_data['vendor'] = str(vendor.id)
        validation_data['image'] = "placeholder_for_validation"

        # validation for incoming data.
        product_details = ProductCreate(**validation_data)

        # delete the existing image from s3
        s3.delete_image(product_obj.image)

        image_url = s3.upload_image(image=image)

        product_details.image = image_url

        product_update = ProductCreate(**input_data)

        for field, value in product_update.dict(exclude_unset=True).items():
            setattr(product_obj, field, value)
        product_obj.save()

        response_data = ProductCreateUpdateResponse(
            id=str(product_obj.id),
            name=product_obj.name,
            description=product_obj.description,
            image=product_obj.image,
            price=product_obj.price,
            category=product_obj.category.to_dict(),
            status=product_obj.status,
            size=product_obj.size.to_dict() if product_obj.size else None,
            color=product_obj.color.to_dict() if product_obj.color else None,
            type=product_obj.type.to_dict(),
        )

        return respond_success(
            message='Product updated successfully',
            data=response_data.dict(),
            status_code=200,
            success=True
        )

    else:
        return respond_error(
            data=None,
            status_code=400,
            message='Current vendor is not the owner of the product.',
            success=False
        )
