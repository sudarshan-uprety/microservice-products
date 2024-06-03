from mongoengine import ReferenceField

from mongoengine import Document


class Vendors(Document):
    user_id = str

    meta = {"collection": "vendors"}

    def __str__(self):
        return str(self.user_id)
