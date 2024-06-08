from mongoengine import StringField, BooleanField, DateTimeField

from models.base import CommonDocument


class Type(CommonDocument):
    """Category model"""
    name = StringField()
    description = StringField()
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
