from mongoengine import Document, DateTimeField
from typing import TypeVar, get_type_hints
import datetime

INVISIBLE = TypeVar('INVISIBLE')

class Base(Document):
    """每次都写get_base_info好烦"""
    meta = {'allow_inheritance': True}
    def get_base_info(self):
        return dict(
            [(k, v) for k, v in vars(self).items() if not get_type_hints(self).get(k, None) == INVISIBLE] +
            [("id", str(self.id))]
        )

class SaveTimeBase(Base):
    meta = {'allow_inheritance': True}
    last_modify = DateTimeField()
    def save_changes(self):
        self.last_modify = datetime.datetime.now()
        return self.save()
    
