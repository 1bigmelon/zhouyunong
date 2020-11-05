import datetime
import hashlib
from mongoengine import *
from app.models.Base import SaveTimeBase


class Tag(SaveTimeBase):
    name = StringField()
    org = StringField()
    description = StringField()
    click = IntField()
    visible = BooleanField()
    publish = BooleanField()

    @staticmethod
    def get_or_create(name):
        _t = Tag.objects(name=name)
        if any(_t):
            return _t.first()
        else:
            return Tag(
                name=name,
                last_modify=datetime.datetime.now()
            ).save()
