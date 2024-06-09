import boto3
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from schema import user
from utils.exception_decorator import error_handler
from utils.response import respond_error, respond_success
from utils import constant, variables, helpers


@error_handler
def main(event: LambdaContext, context: LambdaContext):
    path = event.get("path")

    if path == "/user/change/password":
        return change_password(event, context)
    elif path == "/user/update/phone":
        return update_phone(event, context)
    elif path == "/user/update/address":
        return update_address(event, context)
    elif path == "/user/update/name":
        return update_name(event, context)
    elif path == "/user/forget/password":
        return forget_password(event, context)
    elif path == "/user/confirm/forget/password":
        return confirm_forget_password(event, context)
    else:
        return respond_error(
            status_code=constant.ERROR_BAD_REQUEST,
            message="Invalid path",
            data=None,
            success=False,
            errors=None
        )


def change_password(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validation for incoming data.
    new_detail = user.ChangePassword(**input_data)

    # create a boto3 object
    client = helpers.boto3_client()

    # change user password with cognito
    response = client.change_password(
        PreviousPassword=new_detail.current_password,
        ProposedPassword=new_detail.new_password,
        AccessToken=new_detail.access_token
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return respond_success(
            success=True,
            status_code=constant.SUCCESS_RESPONSE,
            data=None,
            message="Password changed successfully",
            warning=None
        )
    # else condition will be handler by @error_handler decorator.


def update_name(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    new_details = user.UpdateName(**input_data)

    # create a boto client
    client = helpers.boto3_client()

    response = client.update_user_attributes(
        UserAttributes=[
            {
                'Name': 'name',
                'Value': new_details.name
            },
        ],
        AccessToken=new_details.access_token
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return respond_success(
            success=True,
            status_code=constant.SUCCESS_RESPONSE,
            data=None,
            message="Name updated successfully",
            warning=None
        )

    # else condition will be handler by @error_handler decorator.


def update_phone(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    new_details = user.UpdatePhone(**input_data)

    # create a boto client
    client = helpers.boto3_client()

    response = client.update_user_attributes(
        UserAttributes=[
            {
                'Name': 'phone',
                'Value': new_details.phone
            },
        ],
        AccessToken=new_details.access_token
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return respond_success(
            success=True,
            status_code=constant.SUCCESS_RESPONSE,
            data=None,
            message="Phone updated successfully",
            warning=None
        )

    # else condition will be handler by @error_handler decorator.


def update_address(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    new_details = user.UpdateAddress(**input_data)

    # create a boto client
    client = helpers.boto3_client()

    response = client.update_user_attributes(
        UserAttributes=[
            {
                'Name': 'address',
                'Value': new_details.address
            },
        ],
        AccessToken=new_details.access_token
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return respond_success(
            success=True,
            status_code=constant.SUCCESS_RESPONSE,
            data=None,
            message="Address updated successfully",
            warning=None
        )

    # else condition will be handler by @error_handler decorator.


def forget_password(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validating incoming data
    details = user.ForgetPassword(**input_data)

    client = helpers.boto3_client()

    response = client.forgot_password(
        ClientId=variables.CognitoClientId,
        Username=details.username,
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return respond_success(
            success=True,
            status_code=constant.SUCCESS_RESPONSE,
            data=None,
            message="Code has been sent to your email.",
            warning=None
        )

    # else condition will be handler by @error_handler decorator.


def confirm_forget_password(event: LambdaContext, context: LambdaContext):
    input_data = helpers.load_json(event=event)

    # validate incoming data
    data = user.ForgetPasswordConfirm(**input_data)

    # creating a boto client
    client = helpers.boto3_client()

    response = client.confirm_forgot_password(
        ClientId=variables.CognitoClientId,
        Username=data.username,
        ConfirmationCode=data.code,
        Password=data.password
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return respond_success(
            success=True,
            status_code=constant.SUCCESS_RESPONSE,
            data=None,
            message="Password reset successfully.",
            warning=None
        )
    # else condition will be handler by @error_handler decorator.
