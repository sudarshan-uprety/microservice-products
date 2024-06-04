from mongoengine import StringField, DateTimeField
from mongoengine import Document

from models.base import CommonDocument


class Size(CommonDocument):
    name = StringField()

    meta = {"collection": "sizes"}

    def __str__(self):
        return self.name
