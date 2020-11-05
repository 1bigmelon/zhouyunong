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
from app.models.Class import Class
from app.util.auth import generate_jwt, verify_jwt

class_blueprint = Blueprint('class', __name__, url_prefix='/class')

@class_blueprint.before_request
def before_request():
    try:
        if request.get_data():
            g.data = request.get_json(silent=True)
        Authorization = request.headers.get('Authorization', None)
        print(Authorization)
        if Authorization:
            token = Authorization
            g.token = token
            g.user, msg = verify_jwt(token)
        else:
            pass
    except:
        traceback.print_exc()
        return falseReturn(None, '数据错误')

@handle_error
@class_blueprint.route('/modify', methods=['POST'])
@verify_params(params=['name', 'org', 'description', 'subordinate'])
@validsign
@validcall(2048)
def modify_class():
    c = Class.get_or_create(g.data['name'])
    c.org = g.data['org']
    c.description = g.data['description']
    c.subordinate = g.data['subordinate']
    c.last_modify = datetime.datetime.now()
    c.modifier = g.user
    c.save()
    return trueReturn()

@handle_error
@class_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['name'])
@validsign
@validcall(2048)
def remove_class():
    c = Class.objects(g.data['name'])
    c.delete()
    return trueReturn()

@handle_error
@class_blueprint.route('/info', methods=['POST'])
@verify_params(params=['name'])
@validsign
@validcall(2048)
def info_class():
    c = Class.objects(g.data['name'])
    return trueReturn({'info':c.get_base_info()})

@handle_error
@class_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(2048)
def ls_class():
    return trueReturn({'classes':[i.get_base_info() for i in Class.objects()]})
