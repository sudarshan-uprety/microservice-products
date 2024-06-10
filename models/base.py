from datetime import datetime
from mongoengine import Document, DateTimeField, BooleanField


class CommonDocument(Document):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_deleted = BooleanField(default=False)

    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super(CommonDocument, self).save(*args, **kwargs)
