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
from app.util.auth import generate_jwt, verify_jwt, general_before_request

tag_blueprint = Blueprint('tag', __name__, url_prefix='/tag')

@tag_blueprint.before_request
def before_request():
    return general_before_request()

@handle_error
@tag_blueprint.route('/new', methods=['POST'])
@verify_params(params=['name', 'org', 'description'])
@validsign
@validcall(0x1110)
def new_tag():
    t = Tag(name=g.data['name'])
    t.click = 0
    t.org = Org.objects(id=g.data['org']).first()
    t.description = g.data['description']
    t.status = True
    t.save_changes()
    return trueReturn()


@handle_error
@tag_blueprint.route('/modify', methods=['POST'])
@validsign
@validcall(0x1110)
def modify_tag():
    t = Tag.objects(id=g.data['name']).first()
    modifiable = {
        'name', 'description', 'status', 'org'
    }
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            if k == 'org':
                modify_keys[k] = Org.objects(id=v).first()
            else:
                modify_keys[k] = v

    t.modify(**modify_keys)
    t.save_changes()
    return trueReturn()

@handle_error
@tag_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def remove_tag():
    t = Tag.objects(id=g.data['id']).first()
    if not t: return falseReturn(msg='无此标签')
    t.delete()
    return trueReturn()

@handle_error
@tag_blueprint.route('/info', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def info_tag():
    t = Tag.objects(id=g.data['id']).first()
    if not t: return falseReturn(msg='无此标签')
    return trueReturn(t.get_base_info())

@handle_error
@tag_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(0x1110)
def ls_tag():
    return trueReturn({'tags':[i.get_base_info() for i in Tag.objects()]})
