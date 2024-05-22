from mongoengine_goodjson import Document
from mongoengine import StringField, BooleanField


class Category(Document):
    """Category model"""
    name = StringField()
    description = StringField()
    status = BooleanField(default=True)

    meta = {"collection": "categories"}

    def __str__(self):
        return self.name
