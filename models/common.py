from mongoengine.fields import DateTimeField
from mongoengine_goodjson import Document


class Common(Document):
    """Common model"""
    created_at = DateTimeField()
    updated_at = DateTimeField()