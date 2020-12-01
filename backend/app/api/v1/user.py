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
from app.models.Org import Org
from app.util.auth import generate_jwt, verify_jwt, general_before_request

auth_dict = {
    '终审':0x1000,
    '二审':0x100,
    '一审':0x10
}

def encrypt(s):
    return hashlib.sha256(hashlib.sha256(s.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

@user_blueprint.before_request
def before_request():
    return general_before_request()

@handle_error
@user_blueprint.route('/new', methods=['POST'])
@verify_params(params=['name', 'user_id', 'password', 'tel', 'phone', 'email', 'role', 'org'])
@validsign
@validcall(0x1110)
def new_user():
    if g.data['role'] not in auth_dict: return falseReturn(msg='角色未定义')
    u = User.objects(user_id=g.data['user_id'])
    if u: return falseReturn(msg='该用户名已存在')
    o = Org.objects(id=g.data['org']).first()
    if not o: return falseReturn(msg='组织不存在')
    User(
        name=g.data['name'],
        user_id=g.data['user_id'],
        phone=g.data['phone'],
        tel=g.data['tel'],
        email=g.data['email'],
        org=o,
        authority=auth_dict[g.data['role']],
        password=encrypt(g.data['password'])
    ).save_changes()
    return trueReturn()

@handle_error
@user_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def remove_user():
    u = User.objects(id=g.data['id']).first()
    if not u: return falseReturn(msg='用户不存在')
    u.delete()
    return trueReturn()

@handle_error
@user_blueprint.route('/chinfo', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def chinfo_user():
    u = User.objects(id=g.data['id']).first()
    if not u: return falseReturn(msg='用户不存在')
    modifiable = {
        'name', 'role', 'org', 'status',
        'phone', 'tel', 'email', 'role'
    }
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            modify_keys[k] = v
    if 'org' in modify_keys:
        modify_keys['org'] = Org.objects(modify_keys['org']).first()
    if 'role' in modify_keys:
        modify_keys['authority'] = auth_dict[modify_keys['role']]
        modify_keys.pop('role')
    if not modify_keys: return falseReturn(msg='未提供有效的修改指示，什么都没发生')
    u.modify(**modify_keys)
    u.save_changes()
    return trueReturn()

@handle_error
@user_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(0x1110)
def ls_user():
    us = User.objects()
    disabled = User.objects(status=False)
    return trueReturn({
        'users':[i.get_base_info() for i in us],
        'disabled': len(disabled),
        'enabled': len(us) - len(disabled)
    })

@handle_error
@user_blueprint.route('/search', methods=['POST'])
@validsign
@validcall(0x1110)
def search_user():
    sd = {
        'name', 'role', 'org', 'status'
    }
    ks = {}
    for k, v in g.data.items():
        if k in sd:
            if k == 'role':
                ks['authority'] = auth_dict[v]
            elif k == 'org':
                ks['org'] = Org.objects(name=v).first()
            else:
                ks[k] = v

    u = User.objects(**ks)
    return trueReturn({'users':[i.get_base_info() for i in u]})

@handle_error
@user_blueprint.route('/info', methods=['POST'])
@verify_params(params=['user_id'])
@validsign
@validcall(0x1110)
def info_user():
    u = User.objects(user_id=g.data['user_id']).first()
    if not u: return falseReturn(msg='无此用户')
    return trueReturn(u.get_base_info())