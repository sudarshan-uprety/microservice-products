from mongoengine import ReferenceField
from mongoengine import Document

from models.base import CommonDocument


class Vendors(CommonDocument):
    user_id = str

    meta = {"collection": "vendors"}

    def __str__(self):
        return str(self.user_id)
