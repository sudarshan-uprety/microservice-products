from mongoengine import DateTimeField, StringField, FloatField, BooleanField, IntField, ImageField

from mongoengine_goodjson import Document


class Products(Document):
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
