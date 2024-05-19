from mongoengine import DateTimeField, StringField, FloatField, BooleanField, IntField, ImageField

from models.common import Common


class Products(Common):
    """Product Model"""
    name = StringField()
    price = FloatField()
    description = StringField()
    image = ImageField()
    category = StringField()
    stock = IntField()
    status = BooleanField()
    vendor = StringField()

    meta = {"collection": "products"}

    def __str__(self):
        return self.name
