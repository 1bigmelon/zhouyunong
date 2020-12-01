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
from app.models.Article import Div
from app.models.Org import Org
from app.util.auth import generate_jwt, verify_jwt, general_before_request

div_blueprint = Blueprint('div', __name__, url_prefix='/div')

@div_blueprint.before_request
def before_request():
    return general_before_request()

@handle_error
@div_blueprint.route('/new', methods=['POST'])
@verify_params(params=['name', 'org', 'description'])
@validsign
@validcall(0x1110)
def new_div():
    d = Div(name=g.data['name'])
    d.click = 0
    d.org = Org.objects(id=g.data['org']).first()
    d.description = g.data['description']
    d.status = True
    d.save_changes()
    return trueReturn()

@handle_error
@div_blueprint.route('/modify', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def modify_div():
    d = Div.objects(id=g.data['id']).first()
    modifiable = {
        'name', 'org', 'status', 'description'
    }
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            if k == 'org':
                modify_keys[k] = Org.objects(id=v).first()
            else:
                modify_keys[k] = v
    d.modify(**modify_keys)
    d.save_changes()
    return trueReturn()

@handle_error
@div_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def remove_div():
    d = Div.objects(g.data['id']).first()
    if not d: return falseReturn(msg='无此分类')
    d.delete()
    return trueReturn()

@handle_error
@div_blueprint.route('/info', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def info_div():
    d = Div.objects(g.data['id']).first()
    if not d: return falseReturn(msg='无此分类')
    return trueReturn(d.get_base_info())

@handle_error
@div_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(0x1110)
def ls_div():
    return trueReturn({'divs':[i.get_base_info() for i in Div.objects()]})
