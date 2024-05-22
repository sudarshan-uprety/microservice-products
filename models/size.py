from mongoengine import StringField

from mongoengine import Document


class Size(Document):
    name = StringField()
    size = StringField()

    meta = {"collection": "sizes"}

    def __str__(self):
        return self.name
