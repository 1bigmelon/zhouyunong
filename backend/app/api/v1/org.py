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
from app.models.Article import Tag
from app.models.Org import Org
from app.util.auth import generate_jwt, verify_jwt, general_before_request

org_blueprint = Blueprint('org', __name__, url_prefix='/org')

@org_blueprint.before_request
def before_request():
    return general_before_request()


@handle_error
@org_blueprint.route('/new', methods=['POST'])
@verify_params(params=['name', 'description'])
@validsign
@validcall(0x1110)
def new_org():
    o = Org(name=g.data['name'])
    o.description = g.data['description']
    o.status = True
    o.save_changes()
    return trueReturn()

@handle_error
@org_blueprint.route('/modify', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def modify_org():
    o = Org.objects(id=g.data['id']).first()
    modifiable = {
        'name', 'description', 'status'
    }
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            modify_keys[k] = v

    o.modify(**modify_keys)
    o.save_changes()
    return trueReturn()

@handle_error
@org_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def remove_org():
    o = Org.objects(id=g.data['id'])
    if not o: return falseReturn(msg='无此组织')
    o.delete()
    return trueReturn()


@handle_error
@org_blueprint.route('/info', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def info_org():
    o = Org.objects(id=g.data['id']).first()
    if not o: return falseReturn(msg='无此组织')
    return trueReturn(o.get_base_info())

@handle_error
@org_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(0x1110)
def ls_org():
    return trueReturn({'orgs':[i.get_base_info() for i in Org.objects()]})
