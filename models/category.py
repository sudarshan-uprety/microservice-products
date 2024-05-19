from models.common import Common
from mongoengine import StringField, BooleanField


class Category(Common):
    """Category model"""
    name = StringField()
    description = StringField()
    status = BooleanField(default=True)

    meta = {"collection": "categories"}

    def __str__(self):
        return self.name
