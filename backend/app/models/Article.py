from mongoengine import *
from app.models.User import User
from app.models.Org import Org
from typing import List
from app.models.Base import Base, SaveTimeBase, INVISIBLE
import datetime

class Div(SaveTimeBase):
    name = StringField()
    org = ReferenceField(Org, reverse_delete_rule=2)
    status = BooleanField(default=True)
    description = StringField()
    click = IntField()

    @staticmethod
    def get_or_create(name):
        _t = Div.objects(name=name)
        if any(_t):
            return _t.first()
        else:
            return Div(
                name=name,
                last_modify=datetime.datetime.now()
            ).save_changes()

class Tag(SaveTimeBase):
    name = StringField()
    org = ReferenceField(Org, reverse_delete_rule=2)
    description = StringField()
    click = IntField()
    status = BooleanField(default=True)

    @staticmethod
    def get_or_create(name):
        _t = Tag.objects(name=name)
        if any(_t):
            return _t.first()
        else:
            return Tag(
                name=name,
                last_modify=datetime.datetime.now()
            ).save_changes()

class Contrib(SaveTimeBase):
    title = StringField()
    author = StringField()
    status = StringField(default="未审核")
    create_time = DateTimeField()
    contact = StringField()
    org = ReferenceField(Org, reverse_delete_rule=2)

    content = StringField()

    def convert_to_article(self, div: Div, tags: List[Tag]):
        a = Article(
            title=self.title,
            author=self.author,
            create_time=self.create_time,
            status="待一审",
            org=self.org,
            div=div,
            tags=tags,
            content=self.content,
            contact=self.contact
        )
        a.save_changes()
        self.delete()



class Article(SaveTimeBase):
    title = StringField()
    content:INVISIBLE = StringField() # 节约流量
    div = ReferenceField(Div, reverse_delete_rule=2)
    org = ReferenceField(Org, reverse_delete_rule=2)
    author = StringField()
    create_time = DateTimeField()
    email = StringField()
    status = StringField(default='储存库')
    """[储存库, 待一审, 待二审, 待终审, 待发布, 已发布]"""
    pin = BooleanField(default=False)
    tags = ListField(ReferenceField(Tag, reverse_delete_rule=4))
    
    @staticmethod
    def search_visibles(**kwargs) -> list:
        return [i for i in Article.objects(**kwargs) if i.is_me_visible()]

    def is_me_visible(self) -> bool:
        s = self.status == '已发布' and self.div.status
        # print(s)
        if self.org: s = s and self.org.status
        for i in self.tags: s = s and i.status
        # print(s)
        return s

    
    # meta = {'allow_inheritance': True}


