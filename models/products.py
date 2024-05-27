from mongoengine import DateTimeField, StringField, FloatField, BooleanField, IntField, ReferenceField
from mongoengine_goodjson import Document

from models import category, size, color


class Products(Document):
    """Product Model"""
    name = StringField()
    price = FloatField()
    description = StringField()
    image = StringField()
    category = ReferenceField(category.Category)
    stock = IntField()
    status = BooleanField()
    size = ReferenceField(size.Size)
    color = ReferenceField(color.Color)
    vendor = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    meta = {"collection": "products"}

    def __str__(self):
        return self.name
