from mongoengine import StringField, BooleanField, DateTimeField

from models.base import CommonDocument


class Category(CommonDocument):
    """Category model"""
    name = StringField()
    description = StringField()
    status = BooleanField(default=True)

    meta = {"collection": "categories"}

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "status": self.status
        }
