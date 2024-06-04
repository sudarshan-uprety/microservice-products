from mongoengine_goodjson import Document
from mongoengine import StringField, BooleanField, DateTimeField

from models.base import CommonDocument


class Category(CommonDocument):
    """Category model"""
    name = StringField()
    description = StringField()
    status = BooleanField(default=True)
    # created_at = DateTimeField()
    # updated_at = DateTimeField()

    meta = {"collection": "categories"}

    def __str__(self):
        return self.name
