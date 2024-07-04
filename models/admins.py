from models.base import CommonDocument
from mongoengine import StringField, BooleanField, EmailField


class Admin(CommonDocument):
    id = StringField(primary_key=True)
    name = StringField()
    username: StringField(unique=True)
    address = StringField()
    city = StringField()
    state = StringField()
    phone = StringField()
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)

    meta = {"collection": "admins"}

    def __str__(self):
        return str(self.name)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "email": self.email,
            "is_active": self.is_active,
        }
