import datetime
import hashlib
from mongoengine import *
from app.models.Base import Base


class Tag(Base):
    name = StringField()
    organization = StringField()
    description = StringField()
    last_modify = DateTimeField()
    click = IntField()
    visible = BooleanField()

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
