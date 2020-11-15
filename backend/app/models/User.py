import datetime
import hashlib
from app.models.UserBase import UserBase
from app.models.Base import SaveTimeBase
from mongoengine import *
from app.models.Base import INVISIBLE
from app import db

def encrypt(s):
    return hashlib.sha256(hashlib.sha256(s.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()

class User(SaveTimeBase):
    """
    reverse_delete_rule ==> 引用对象被删除时：
    0：啥也不干
    1：将所有对此的引用空化(整个List都会被爆破)
    2：删除引用此的文档（是整个删除不是只删引用
    3：如果有别的东西引用这个，阻止删除操作
    4：只对ListField套ReferenceField有用，两层List不行，表现与0相同；没有List套会报错；删除引用对象后如同.remove这个元素
    """
    name = StringField()
    user_id: INVISIBLE = StringField() # 登录凭据
    password: INVISIBLE = StringField()
    role = StringField(default='游客')
    dep = StringField()
    contact = StringField()
    email = StringField()
    status = StringField()
    last_ip = StringField()
    last_login = DateTimeField(default=datetime.datetime.now())
    authority: INVISIBLE = IntField(default=0)
    # roles = db.ListField(db.ReferenceField(Role,reverse_delete_rule=4),default=[])

    def valid_password(self, password):
        return self.password == encrypt(password)

    @staticmethod
    def get_or_create(user_id, **kwargs): # 表格导入的时候防重
        _t = User.objects(user_id=user_id)
        if any(_t):
            return _t.first()
        else:
            return User(
                user_id=user_id,
                last_modify=datetime.datetime.now(),
                **kwargs
            ).save()

    # def get_base_info(self):
    #     print(self._fields_ordered)
    #     return dict(
    #         [(k, v) for k, v in vars(self).items() if not get_type_hints(self).get(k, None) == INVISIBLE] +
    #         [("id", str(self.id))]
    #     )
