from mongoengine import StringField, IntField, BooleanField
from mongoengine_goodjson import Document

from models.base import CommonDocument


class Color(CommonDocument):
    """Color model"""
    name = StringField()
    color = StringField()
    hex = StringField()
    status = BooleanField(default=True)

    meta = {"collection": "colors"}

    def __str__(self):
        return self.name
