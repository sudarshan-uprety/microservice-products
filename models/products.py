from mongoengine import StringField, FloatField, BooleanField, IntField, ReferenceField, ListField, EmbeddedDocumentListField

from models import category, size, color, type, vendors
from models.base import CommonDocument


class ProductVariant(CommonDocument):
    size = ReferenceField(size.Size, required=False, null=True)
    color = ReferenceField(color.Color, required=False, null=True)
    stock = IntField(default=0)

    def to_dict(self):
        return {
            "id": str(self.id),
            "size": str(self.size.id) if self.size else None,
            "color": str(self.color.id) if self.color else None,
            "stock": self.stock
        }


class Products(CommonDocument):
    """Product Model"""
    name = StringField()
    price = FloatField()
    description = StringField()
    image = ListField(StringField())
    category = ReferenceField(category.Category)
    status = BooleanField(default=True)
    type = ReferenceField(type.Type)
    vendor = ReferenceField(vendors.Vendors, required=True)
    variants = ListField(ReferenceField(ProductVariant))

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
            "status": self.status,
            "type": str(self.type.id) if self.type else None,
            "vendor": str(self.vendor.id) if self.vendor else None,
            "variants": [variant.to_dict() for variant in self.variants]
        }

    def total_stock(self):
        return sum(variant.stock for variant in self.variants)
