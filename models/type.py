from mongoengine import StringField, BooleanField, ReferenceField

from models.base import CommonDocument
from models import admins


class Type(CommonDocument):
    """Category model"""
    name = StringField()
    description = StringField()
    created_by = ReferenceField(admins.Admin)
    status = BooleanField(default=True)

    meta = {"collection": "types"}

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": str(self.id),
            'name': self.name,
            'description': self.description,
            'status': self.status,
        }
