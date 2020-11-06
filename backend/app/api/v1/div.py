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
from app.util.auth import generate_jwt, verify_jwt, general_before_request()

div_blueprint = Blueprint('div', __name__, url_prefix='/div')

@div_blueprint.before_request
def before_request():
    return general_before_request()

@handle_error
@div_blueprint.route('/modify', methods=['POST'])
@verify_params(params=['name', 'org', 'description', 'subordinate'])
@validsign
@validcall(2048)
def modify_div():
    c = Class.get_or_create(g.data['name'])
    c.org = g.data['org']
    c.description = g.data['description']
    c.subordinate = g.data['subordinate']
    c.modifier = g.user
    c.save_changes()
    return trueReturn()

@handle_error
@div_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['name'])
@validsign
@validcall(2048)
def remove_div():
    c = Class.objects(g.data['name'])
    if not c: return falseReturn(msg='无此分类')
    c.delete()
    return trueReturn()

@handle_error
@div_blueprint.route('/info', methods=['POST'])
@verify_params(params=['name'])
@validsign
@validcall(2048)
def info_div():
    c = Class.objects(g.data['name']).first()
    if not c: return falseReturn(msg='无此分类')
    return trueReturn(c.get_base_info())

@handle_error
@div_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(2048)
def ls_div():
    return trueReturn({'divs':[i.get_base_info() for i in Div.objects()]})
