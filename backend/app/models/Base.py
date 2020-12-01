from mongoengine import Document, DateTimeField
from typing import TypeVar, get_type_hints
import datetime

INVISIBLE = TypeVar('INVISIBLE')

class Base(Document):
    """每次都写get_base_info好烦"""
    meta = {'allow_inheritance': True}
    def get_base_info(self, *args):
        # print(vars(self))
        return dict(
            [(k, getattr(getattr(self, k), 'get_base_info', lambda x:x)(getattr(self, k))) for k in self._fields_ordered if not get_type_hints(self).get(k, None) == INVISIBLE] +
            [("id", str(self.id))]
        )

    def get_all_info(self, *args):
        # print(vars(self))
        return dict(
            [(k, getattr(self, k)) for k in self._fields_ordered] +
            [("id", str(self.id))]
        )

class SaveTimeBase(Base):
    meta = {'allow_inheritance': True}
    last_modify = DateTimeField()
    def save_changes(self):
        self.last_modify = datetime.datetime.now()
        return self.save()
    
