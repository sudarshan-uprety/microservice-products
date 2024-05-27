from mongoengine import StringField, DateTimeField

from mongoengine import Document


class Size(Document):
    name = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    meta = {"collection": "sizes"}

    def __str__(self):
        return self.name
