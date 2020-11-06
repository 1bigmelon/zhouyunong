import datetime
import hashlib
import json
import traceback

import requests
from flask import Blueprint
from flask import current_app as flaskapp
from flask import g, jsonify, request
from mongoengine.queryset.visitor import Q

from app.api import handle_error, validsign, verify_params, validcall
from app.common.result import falseReturn, trueReturn
from app.models.User import User
from app.util.auth import generate_jwt, verify_jwt, general_before_request

def encrypt(s):
    return hashlib.sha256(hashlib.sha256(s.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

@user_blueprint.before_request
def before_request():
    return general_before_request()

@handle_error
@user_blueprint.route('/new', methods=['POST'])
@verify_params(params=['name', 'user_id', 'password', 'contact', 'email', 'authority', 'dep'])
@validsign
def new_user():
    u = User.objects(user_id=g.data['user_id'])
    if u: return falseReturn(msg='该用户名已存在')
    if g.data['authority'] >= g.user.authority: return falseReturn(msg='只能创建权限比自己小的用户')
    User(
        name=g.data['name'],
        user_id=g.data['user_id'],
        contact=g.data['contact'],
        email=g.data['email'],
        authority=g.data['authority'],
        dep=g.data['dep'],
        password=encrypt(g.data['password'])
    ).save()
    return trueReturn()

@handle_error
@user_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
def remove_user():
    u = User.objects(g.data['id']).first()
    if not u: return falseReturn(msg='用户不存在')
    if g.user.authority <= u.authority:
        return falseReturn(msg='您只能删除权限小于自己的用户')
    u.delete()
    return trueReturn()

@handle_error
@user_blueprint.route('/chinfo', methods=['POST'])
@verify_params(params=['id'])
@validsign
def chinfo_user():
    u = User.objects(g.data['id']).first()
    if g.user.authority <= u.authority:
        return falseReturn(msg='您只能修改权限小于自己的用户')
    modifiable = {'name', 'role', 'dep', 'status', 'contact', 'email', 'authority'}
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            modify_keys[k] = v
    if modify_keys.get('authority', 0) >= g.user.authority: return falseReturn(msg='您不能赋予他人高于或等于自己的权限')
    u.modify(**modify_keys)
    u.save_changes()
    return trueReturn()

@handle_error
@user_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(2048)
def ls_user():
    return trueReturn({'users':[i.get_base_info() for i in User.objects()]})

@handle_error
@user_blueprint.route('/info', methods=['POST'])
@verify_params(params=['user_id'])
@validsign
def info_user():
    u = User.objects(user_id=g.data['user_id']).first()
    if not u: return falseReturn(msg='无此用户')
    return trueReturn(u.get_base_info())