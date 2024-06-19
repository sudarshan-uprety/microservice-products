from models.base import CommonDocument
from mongoengine import StringField, BooleanField


class Vendors(CommonDocument):
    id = StringField(primary_key=True)
    store_name = StringField()
    address = StringField()
    city = StringField()
    state = StringField()
    phone = StringField()
    email = StringField()
    is_active = BooleanField(default=False)

    meta = {"collection": "vendors"}

    def __str__(self):
        return str(self.store_name)

    def to_dict(self):
        return {
            "vendor_id": self.id,
            "store_name": self.store_name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "email": self.email,
            "is_active": self.is_active,
        }
