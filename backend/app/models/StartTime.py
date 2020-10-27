import datetime
import hashlib
from app import db


def str2md5(str):
    return hashlib.sha256(hashlib.sha256(str.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()


class StartTime(db.Document):

    server_starttime = db.DateTimeField()  # 服务器开始运行的时间，后面用于判断签到周

    def change_starttime(self, t):  # 记得做这个接口
        self.server_starttime = t
        return self.save()

    def init_starttime():
        s = StartTime.objects()
        if not s:
            return StartTime(server_starttime = datetime.datetime.now()).save()
        else:
            t = s.first()
            t.server_starttime = datetime.datetime.now()
            return t.save()


    def get_base_info(self):
        return {"server_starttime": self.server_starttime}
