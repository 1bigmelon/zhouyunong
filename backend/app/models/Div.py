import datetime
import hashlib
from mongoengine import *
from app.models.Base import SaveTimeBase
from app.models.User import User

class Div(SaveTimeBase):
    name = StringField()
    org = StringField()
    subordinate = StringField()
    description = StringField()
    modifier = ReferenceField(User)
    click = IntField()
    publish = BooleanField()

    @staticmethod
    def get_or_create(name):
        _t = Div.objects(name=name)
        if any(_t):
            return _t.first()
        else:
            return Div(
                name=name,
                last_modify=datetime.datetime.now()
            ).save()
