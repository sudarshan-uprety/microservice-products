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

    if path == "/user/login":
        return login_user(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def login_user(event: LambdaContext, context: LambdaContext):
    body = event.get('body')

    if not body:
        return respond_error(
            status_code=400,
            message="Missing body",
            data=None,
            success=False
        )

    login_details = json.loads(body)

    # validation for incoming product data.
    input_data = user.Login(**login_details)

    # create a boto3 object
    client = boto3.client('cognito-idp', region_name=variables.CognitoRegionName)

    # Register user in cognito
    response = client.initiate_auth(
        ClientId=variables.CognitoClientId,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': input_data.username,
            'PASSWORD': input_data.password
        }
    )

    # Return success response
    return respond_success(
        status_code=constant.SUCCESS_RESPONSE,
        success=True,
        data={
            'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken'],
            },
        warning=None,
        message="Fetched access and refresh token",
    )
