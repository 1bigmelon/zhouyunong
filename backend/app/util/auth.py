import jwt
import time
import datetime
import traceback
from app.common.result import falseReturn, trueReturn
from flask import current_app
from flask import g, jsonify, request
from app.models.User import User

def generate_jwt(user):
    token_dict = {
        'iat': time.time(), # 1天
        'id': str(user.id)
    }
    return jwt.encode(token_dict,  # payload, 有效载体
                      current_app.config['JWT_SECRET'],  # 进行加密签名的密钥
                      algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                      ).decode()  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str

def verify_jwt(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithm=['HS256'])
        if payload['iat'] < time.time() - 60*60*24:
            return None, "登入超时"
        # print(payload['id'])
        user = User.objects(id=payload['id']).first()
        # print(user.get_base_info())
        # print(payload['iat'])
        # print(user.pw_updated.timestamp())
        if payload['iat'] < user.pw_updated.timestamp():
            return None, "密码已修改，请使用新密码重新登录"
        if not user:
            return None, "无此用户"
        return user, ""
    except:
        traceback.print_exc()
        return None, "数据错误"

def general_before_request():
    try:
        if request.get_data():
            g.data = request.get_json(silent=True)
        Authorization = request.headers.get('Authorization', None)
        print(Authorization)
        if Authorization:
            token = Authorization
            g.token = token
            g.user, g.msg = verify_jwt(token)
        else:
            pass
    except:
        traceback.print_exc()
        return falseReturn(None, '数据错误')