import boto3
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from schema import user, admins
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, variables, helpers
from utils.middleware import vendor_check, admin_check
from utils.lambda_middleware import lambda_middleware


@lambda_middleware
@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/vendor/login":
        return login_vendor(event, context)
    if path == "/admin/login":
        return login_admin(event, context)
    elif path == "/user/detail":
        return user_details(event, context)
    elif path == "/admin/detail":
        return admin_details(event, context)
    elif path == "/user/new/token":
        return refresh_token(event, context)
    elif path == "/user/logout":
        return user_logout(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


@vendor_check
def login_vendor(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validation for incoming data.
    login_detail = user.Login(**input_data)

    # create a boto3 object
    client = helpers.boto3_cognito_client()

    # Register user in cognito
    response = client.initiate_auth(
        ClientId=variables.CognitoClientId,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': login_detail.username,
            'PASSWORD': login_detail.password
        }
    )

    # response
    token_response = user.UserToken(
        access_token=response['AuthenticationResult']['AccessToken'],
        refresh_token=response['AuthenticationResult']['RefreshToken'],
        id_token=response['AuthenticationResult']['IdToken'],
    ).dict()

    # Return success response
    return respond_success(
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data=token_response,
        warning=None,
        message="User logged in.",
    )


@admin_check
def login_admin(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validation for incoming data.
    login_detail = user.Login(**input_data)

    # create a boto3 object
    client = helpers.boto3_cognito_client()

    # Register user in cognito
    response = client.initiate_auth(
        ClientId=variables.CognitoClientId,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': login_detail.username,
            'PASSWORD': login_detail.password
        }
    )

    # response
    token_response = user.UserToken(
        access_token=response['AuthenticationResult']['AccessToken'],
        refresh_token=response['AuthenticationResult']['RefreshToken'],
        id_token=response['AuthenticationResult']['IdToken'],
    ).dict()

    # Return success response
    return respond_success(
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data=token_response,
        warning=None,
        message="User logged in.",
    )


def user_details(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validation for incoming data.
    user_detail = user.GetUserDetail(**input_data)

    # boto client
    client = helpers.boto3_cognito_client()

    response = client.get_user(
        AccessToken=user_detail.access_token,
    )

    user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}

    user_detail_response = user.UserDetailResponse(
        username=response['Username'],
        email=user_attributes.get('email', ''),
        phone=user_attributes.get('phone_number', ''),
        address=user_attributes.get('address', ''),
        name=user_attributes.get('name', ''),
    )

    return respond_success(
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data=user_detail_response.dict(),
        message="Fetched user details",
        warning=None
    )


def refresh_token(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    token_detail = user.NewAccessToken(**input_data)

    client = helpers.boto3_cognito_client()

    response = client.initiate_auth(
        ClientId=variables.CognitoClientId,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': token_detail.refresh_token
        }
    )

    response_access_token = user.NewAccessTokenResponse(
        access_token=response['AuthenticationResult']['AccessToken'],
        id_token=response['AuthenticationResult']['IdToken'],

    )

    return respond_success(
        success=True,
        status_code=constant.SUCCESS_RESPONSE,
        data=response_access_token.dict(),
        message="Fetched new access token",
        warning=None
    )


def user_logout(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    token_detail = user.Logout(**input_data)

    client = helpers.boto3_cognito_client()

    response = client.global_sign_out(
        AccessToken=token_detail.access_token
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return respond_success(
            success=True,
            status_code=constant.SUCCESS_RESPONSE,
            data=None,
            message="User logged out",
            warning=None
        )

    # else condition will be handler by @error_handler decorator.


def admin_details(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validation for incoming data.
    admin_detail = admins.GetAdminDetail(**input_data)

    # boto client
    client = helpers.boto3_cognito_client()

    response = client.get_user(
        AccessToken=admin_detail.access_token,
    )

    user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}

    user_detail_response = admins.AdminDetailResponse(
        username=response['Username'],
        email=user_attributes.get('email', ''),
        phone=user_attributes.get('phone_number', ''),
        address=user_attributes.get('address', ''),
        name=user_attributes.get('name', ''),
        is_superuser=user_attributes.get('custom:is_superuser', ''),
    )

    return respond_success(
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data=user_detail_response.dict(),
        message="Fetched admin details",
        warning=None
    )
