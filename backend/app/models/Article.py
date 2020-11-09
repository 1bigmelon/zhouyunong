from mongoengine import *
from app.models.User import User
from app.models.Base import Base, SaveTimeBase
import datetime

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

class Article(SaveTimeBase):
    title = StringField()
    source = StringField()
    div = ReferenceField(Div)
    author = StringField()
    create_time = DateTimeField()
    email = ListField(StringField())
    status = StringField(default='储存库')
    """[存储库, 回收站, 一审, 二审, 终审, 发布]"""
    pin = BooleanField()
    upload = BooleanField()
    draft = BooleanField()
    writable = ListField(ReferenceField(User, reverse_delete_rule=4))
    readable = ListField(ReferenceField(User, reverse_delete_rule=4))
    tags = ListField(ReferenceField(Tag))
    meta = {'allow_inheritance': True}

    def append_access(self, new_writables=[], new_readables=[]):
        for _ in new_writables:
            self.update(add_to_set__writable=_)
        for _ in new_readables:
            self.update(add_to_set__readable=_)
        return

    def discard_access(self, ban_writables=[], ban_readables=[]):
        for _ in ban_writables:
            self.update(pull__writable=_)
        for _ in ban_readables:
            self.update(pull__readable=_)
        return

    def modify_access(self, new_writables=[], new_readables=[]):
        self.writable = new_writables
        self.readable = new_readables
        return self.save()
