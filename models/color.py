from mongoengine import StringField, IntField, BooleanField
from mongoengine_goodjson import Document

from models.base import CommonDocument


class Color(CommonDocument):
    """Color model"""
    name = StringField()
    hex = StringField()
    status = BooleanField(default=True)

    meta = {"collection": "colors"}

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "hex": self.hex,
            "status": self.status,
        }
