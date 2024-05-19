from mongoengine import StringField, IntField, BooleanField

from models.common import Common


class Color(Common):
    """Color model"""
    name = StringField()
    color = StringField()
    hex = StringField()
    status = BooleanField(default=True)

    meta = {"collection": "colors"}

    def __str__(self):
        return self.name
