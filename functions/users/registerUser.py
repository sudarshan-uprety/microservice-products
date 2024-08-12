from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from schema import user, admins
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, variables, helpers, database
from models import vendors
from models.admins import Admin
from utils.middleware import verify_vendor, verify_admin
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/register/user":
        return register_user(event, context)
    elif path == "/verify/user":
        return verify_user(event, context)
    elif path == "/register/admin":
        return register_admin(event, context)
    elif path == "/verify/admin":
        return admin_verify(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def register_user(event: LambdaContext, context: LambdaContext):
    user_details = helpers.load_json(event=event)

    # validation for incoming user data.
    input_data = user.UserRegister(**user_details)

    # create a boto3 object
    client = helpers.boto3_cognito_client()

    # Register user in cognito
    response = client.sign_up(
        ClientId=variables.CognitoClientId,
        Username=input_data.username,
        Password=input_data.password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': input_data.email
            },
            {
                'Name': 'name',
                'Value': input_data.name
            },
            {
                'Name': 'phone_number',
                'Value': input_data.phone
            },
            {
                'Name': 'address',
                'Value': input_data.address
            },
            {
                'Name': 'custom:city',
                'Value': input_data.city
            },
            {
                'Name': 'custom:state',
                'Value': input_data.state
            },
            {
                'Name': 'custom:is_superuser',
                'Value': '0'
            }
        ]
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:

        database.db_config()

        vendor = vendors.Vendors(
            id=response['UserSub'],
            store_name=input_data.name,
            username=input_data.username,
            address=input_data.address,
            city=input_data.city,
            state=input_data.state,
            phone=input_data.phone,
            email=input_data.email,
            is_active=False
        )
        vendor.save()

        response_data = user.UserRegisterResponse(**user_details)

        # Return success response
        return respond_success(
            status_code=constant.SUCCESS_CREATED,
            success=True,
            data=response_data.dict(),
            warning=None,
            message="User registered, please check your email for confirmation.",
        )


@verify_vendor
def verify_user(event: LambdaContext, context: LambdaContext, **kwargs):
    input_data = kwargs['body']

    # validate incoming data
    data = user.VerifyEmail(**input_data)

    client = helpers.boto3_cognito_client()

    response = client.confirm_sign_up(
        ClientId=variables.CognitoClientId,
        Username=data.username,
        ConfirmationCode=data.code
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        vendor = kwargs['vendor']
        vendor.is_active = True
        vendor.save()

    return respond_success(
        message="Email verification successful.",
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data=None,
        warning=None
    )


def register_admin(event: LambdaContext, context: LambdaContext):
    admin_details = helpers.load_json(event=event)

    # validation for incoming admin data.
    input_data = user.UserRegister(**admin_details)

    # create a boto3 object
    client = helpers.boto3_cognito_client()

    # Register admin in cognito
    response = client.sign_up(
        ClientId=variables.CognitoClientId,
        Username=input_data.username,
        Password=input_data.password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': input_data.email
            },
            {
                'Name': 'name',
                'Value': input_data.name
            },
            {
                'Name': 'phone_number',
                'Value': input_data.phone
            },
            {
                'Name': 'address',
                'Value': input_data.address
            },
            {
                'Name': 'custom:city',
                'Value': input_data.city
            },
            {
                'Name': 'custom:state',
                'Value': input_data.state
            },
            {
                'Name': 'custom:is_superuser',
                'Value': "1"
            }
        ]
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:

        database.db_config()

        admin = Admin(
            id=response['UserSub'],
            name=input_data.name,
            username=input_data.username,
            address=input_data.address,
            city=input_data.city,
            state=input_data.state,
            phone=input_data.phone,
            email=input_data.email,
            is_active=False
        )
        admin.save()

        response_data = admins.AdminRegisterResponse(**admin_details)

        # Return success response
        return respond_success(
            status_code=constant.SUCCESS_CREATED,
            success=True,
            data=response_data.dict(),
            warning=None,
            message="Admin is registered, please check email for confirmation.",
        )


@verify_admin
def admin_verify(event: LambdaContext, context: LambdaContext, **kwargs):
    input_data = kwargs['body']

    # validate incoming data
    data = admins.VerifyAdminEmail(**input_data)

    client = helpers.boto3_cognito_client()

    response = client.confirm_sign_up(
        ClientId=variables.CognitoClientId,
        Username=data.username,
        ConfirmationCode=data.code
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        admin = kwargs['admin']
        admin.is_active = True
        admin.save()

    return respond_success(
        message="Email verification successful.",
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data=None,
        warning=None
    )
