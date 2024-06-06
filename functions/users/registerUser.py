import json
import os

import boto3
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from schema import user
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, variables


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/register/user":
        return register_user(event, context)
    elif path == "/verify/user":
        return verify_user(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def register_user(event: LambdaContext, context: LambdaContext):
    body = event.get('body')

    if not body:
        return respond_error(
            status_code=400,
            message="Missing body",
            data=None,
            success=False
        )

    user_details = json.loads(body)

    # validation for incoming product data.
    input_data = user.UserRegister(**user_details)

    # create a boto3 object
    client = boto3.client('cognito-idp',region_name=variables.CognitoRegionName)

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
            }
        ]
    )

    # Return success response
    return respond_success(
        status_code=constant.SUCCESS_CREATED,
        success=True,
        data=input_data.dict(exclude={'password', 'confirm_password'}),
        warning=None,
        message="User registered, please check your email for confirmation.",
    )


def verify_user(event: LambdaContext, context: LambdaContext):
    body = event.get('body')

    if not body:
        return respond_error(
            status_code=400,
            message="Missing body",
            data=None,
            success=False

        )
    user_details = json.loads(body)

    input_data = user.VerifyEmail(**user_details)

    client = boto3.client('cognito-idp', region_name=variables.CognitoRegionName)

    response = client.confirm_sign_up(
        ClientId=variables.CognitoClientId,
        Username=input_data.username,
        ConfirmationCode=input_data.code
    )

    return respond_success(
        message="Email verification successful.",
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data=input_data.dict(exclude={'code'}),
        warning=None
    )
