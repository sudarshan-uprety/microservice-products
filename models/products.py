from mongoengine import StringField, FloatField, BooleanField, IntField, ReferenceField

from models import category, size, color, type
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
    vendor = StringField()

    meta = {"collection": "products"}

    def __str__(self):
        return self.name
