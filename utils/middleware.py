from functools import wraps
from mongoengine import DoesNotExist
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError

from utils.database import db_config

from models.vendors import Vendors
from models.admins import Admin


def admin_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            db_config()
            admin = Admin.objects.get(id=args[0]['requestContext']['authorizer']['claims']['sub'], is_deleted=False)
            if not admin.is_active:
                raise ValueError("Admin is not active")
            kwargs['admin'] = admin
        except DoesNotExist:
            raise DoesNotExist("Admin does not exist")
        return func(*args, **kwargs)
    return wrapper


def vendors_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            db_config()
            vendor = Vendors.objects.get(id=args[0]['requestContext']['authorizer']['claims']['sub'], is_deleted=False)
            if not vendor.is_active:
                raise ValueError("Admin is not active")
            kwargs['admin'] = vendor
        except DoesNotExist:
            raise DoesNotExist("Vendor does not exist")
        return func(*args, **kwargs)
    return wrapper


def update_element(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = args[0]['pathParameters']['id']
        obj_class = kwargs.get("model")
        current_admin = kwargs.get('user')
        try:
            element = obj_class.objects.get(id=id, is_deleted=False)
            if str(element.created_by.id) != str(current_admin.id):
                raise UnauthorizedError("You are not authorized to update/delete this element.")
            kwargs['element'] = element
            return func(*args, **kwargs)
        except DoesNotExist:
            raise DoesNotExist("Element does not exist")
    return wrapper
