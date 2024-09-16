from mongoengine import StringField, BooleanField, ReferenceField

from models.base import CommonDocument
from models import admins


class Size(CommonDocument):
    name = StringField()
    description = StringField()
    status = BooleanField(default=True)
    created_by = ReferenceField(admins.Admin)

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
