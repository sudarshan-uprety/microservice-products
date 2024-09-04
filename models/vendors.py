from models.base import CommonDocument
from mongoengine import StringField, BooleanField, EmailField


class Vendors(CommonDocument):
    id_sub = StringField(unique=True)
    username = StringField(unique=True)
    store_name = StringField()
    address = StringField()
    city = StringField()
    state = StringField()
    phone = StringField()
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)

    meta = {"collection": "vendors"}

    def __str__(self):
        return str(self.store_name)

    def to_dict(self):
        return {
            "vendor_id": str(self.id),
            "id_sub": self.id_sub,
            "store_name": self.store_name,
            "username": self.username,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "email": self.email,
            "is_active": self.is_active,
        }
