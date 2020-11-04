from mongoengine import *
from app.models.UserBase import UserBase
from app.models.Base import Base
from app.models.Tag import Tag
from app.models.Class import Class
import datetime

class Ariticle(Base):
    title = StringField()
    password = StringField(default='')
    last_modify = DateTimeField()
    create_datetime = DateTimeField()
    writable = ListField(ReferenceField(UserBase,reverse_delete_rule=4))
    readable = ListField(ReferenceField(UserBase,reverse_delete_rule=4))
    tags = ListField(ReferenceField(Tag))
    class_ = ReferenceField(Class)
    meta = {'allow_inheritance': True}
    

    def retitle(self,new_title:str) -> self:
        self.title = new_title
        self.last_modify = datetime.datetime.now()
        return self.save()

    def set_password(self,password:str) -> self:
        self.password = password
        return self.save()

    @staticmethod
    def new_article(author: UserBase):
        return Ariticle(writable=[author],readable=[author],last_modify=datetime.datetime.now())

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

    def get_base_info(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "last_modify": self.last_modify,
            "create_datetime": self.create_datetime
        }



