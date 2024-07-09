from mongoengine import StringField, ReferenceField, BooleanField

from models.base import CommonDocument
from models.admins import Admin


class Color(CommonDocument):
    """Color model"""
    name = StringField()
    hex = StringField()
    created_by = ReferenceField(Admin)
    status = BooleanField(default=True)

    meta = {"collection": "colors"}

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "hex": self.hex,
            # "created_by": str(self.created_by.id) if self.created_by else None,
            "status": self.status,
        }
