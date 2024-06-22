from mongoengine import StringField, FloatField, BooleanField, IntField, ReferenceField

from models import category, size, color, type, vendors
from models.base import CommonDocument


class Products(CommonDocument):
    """Product Model"""
    name = StringField()
    price = FloatField()
    description = StringField()
    image = StringField()
    category = ReferenceField(category.Category)
    stock = IntField()
    status = BooleanField(default=True)
    size = ReferenceField(size.Size, required=False, null=True)
    color = ReferenceField(color.Color, required=False, null=True)
    type = ReferenceField(type.Type)
    vendor = ReferenceField(vendors.Vendors, required=True, null=False)

    meta = {"collection": "products"}

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image,
            "category": str(self.category.id) if self.category else None,
            "stock": self.stock,
            "status": self.status,
            "size": str(self.size.id) if self.size else None,
            "color": str(self.color.id) if self.color else None,
            "type": str(self.type.id) if self.type else None,
            "vendor": str(self.vendor.id) if self.vendor else None
        }