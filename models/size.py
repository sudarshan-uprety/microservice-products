from mongoengine import StringField

from models.common import Common


class Size(Common):
    name = StringField()
    size = StringField()

    meta = {"collection": "sizes"}

    def __str__(self):
        return self.name
