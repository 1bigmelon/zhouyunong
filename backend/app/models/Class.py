import datetime
import hashlib
from mongoengine import *
from app.models.Base import Base


class Class(Base):
    name = StringField()
    organization = StringField()
    subordinate = StringField()
    description = StringField()
    last_modify = DateTimeField()
    click = IntField()
    publish = BooleanField()

    @staticmethod
    def get_or_create(name):
        _t = Class.objects(name=name)
        if any(_t):
            return _t.first()
        else:
            return Class(
                name=name,
                last_modify=datetime.datetime.now()
            ).save()
