import datetime
import hashlib
import json
import traceback

import requests
from flask import Blueprint
from flask import current_app as flaskapp
from flask import g, jsonify, request
from mongoengine.queryset.visitor import Q

from app.api import handle_error, validsign, verify_params
from app.common.result import falseReturn, trueReturn
from app.models.User import User, encrypt
from app.util.auth import generate_jwt, verify_jwt, general_before_request

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
"""
个人认为auth这里放登录认证
以及有关本人（不涉及别人）的操作
"""


@auth_blueprint.before_request
def before_request():
    general_before_request()


@handle_error
@auth_blueprint.route('/signin', methods=['POST'])
def signin_auth():
    name = g.data.get("username", "").strip()
    password = g.data.get("password", "")
    user: User = User.objects(user_id=name).first()
    if not user or not user.valid_password(password):
        return falseReturn(None, "用户名或密码有误")
    if not user.status:
        return falseReturn(msg='用户已被停用，请联系管理员')
    if user.org and not user.org.status:
        return falseReturn(msg='该用户所属组织已被停用，请联系管理员')
    user.modify(
        last_ip=request.remote_addr,
        last_login=datetime.datetime.now()
    )
    return trueReturn({
        'user': user.get_base_info(),
        'token': generate_jwt(user),
    })

@handle_error
@auth_blueprint.route('/chinfo', methods=['POST'])
@validsign
def chinfo_auth():
    modifiable = {
        'name', 'tel', 'contact', 'email',
        'phone', 'org'
    }
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            if k == 'org':
                modify_keys[k] = Org.objects(id=v).first()
            else:
                modify_keys[k] = v
    g.user.modify(**modify_keys)
    g.user.last_ip = request.remote_addr
    g.user.save_changes()
    return trueReturn()

@handle_error
@auth_blueprint.route('/verify', methods=['GET'])
@validsign
def verify_auth():
    return trueReturn(g.user.get_base_info())

@handle_error
@auth_blueprint.route('/chpw', methods=['POST'])
@validsign
def chpw_auth():
    old = g.data.get("old", "")
    password = g.data.get("password", "")
    user: User = User.objects().first()
    if not user or not user.valid_password(old):
        return falseReturn(msg="旧密码不匹配")
    user.password = encrypt(password)
    user.pw_updated = datetime.datetime.now()
    user.save_changes()
    return trueReturn({
        'user': user.get_base_info(),
        'token': generate_jwt(user)
    })