import datetime
import hashlib
from mongoengine import *
from app.models.Base import SaveTimeBase

class Org(SaveTimeBase):
    name = StringField()
    description = StringField()
    status = BooleanField(default=True)

