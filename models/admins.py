from models.base import CommonDocument
from mongoengine import StringField, BooleanField


class Admin(CommonDocument):
    id = StringField(primary_key=True)
    name = StringField()
    address = StringField()
    city = StringField()
    state = StringField()
    phone = StringField()
    email = StringField()
    is_active = BooleanField(default=False)

    meta = {"collection": "admins"}

    def __str__(self):
        return str(self.name)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "email": self.email,
            "is_active": self.is_active,
        }
