from mongoengine import StringField, BooleanField

from models.base import CommonDocument


class Size(CommonDocument):
    name = StringField()
    description = StringField()
    status = BooleanField(default=True)

    meta = {"collection": "size"}

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "status": self.status,
        }
