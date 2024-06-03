import json

from mongoengine.errors import DoesNotExist, FieldDoesNotExist, ValidationError
from pydantic import ValidationError as PydanticError

from utils import constant, response, helpers
from utils.exception import ServerError, CustomException


def error_handler(func):
    def validate(*args, **kwargs):
        try:
            to_return = func(*args, **kwargs)
        except DoesNotExist as err:
            return response.error_response(
                status_code=constant.ERROR_NOT_FOUND, message=err.args[0]
            )
        except FieldDoesNotExist as err:
            return response.error_response(
                status_code=constant.ERROR_FOUND, message=err.args[0]
            )
        except ValidationError as err:
            return response.error_response(
                status_code=constant.ERROR_FOUND, message=err.args[0]
            )
        except ServerError as err:
            return response.error_response(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR, message=constant.ERROR_SERVER_DOWN
            )
        except CustomException as err:
            print('hey', err)
            return response.error_response(
                status_code=constant.ERROR_INTERNAL_SERVER_ERROR, message=err.args[0]
            )
        except PydanticError as err:
            msg = helpers.pydantic_error(err)
            return response.error_response(
                status_code=constant.ERROR_BAD_REQUEST, message=msg, errors=[]
            )
        return to_return
    return validate
