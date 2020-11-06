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
from app.models.Tag import Tag
from app.util.auth import generate_jwt, verify_jwt, general_before_request

tag_blueprint = Blueprint('tag', __name__, url_prefix='/tag')

@tag_blueprint.before_request
def before_request():
    return general_before_request()

@handle_error
@tag_blueprint.route('/modify', methods=['POST'])
@verify_params(params=['name', 'org', 'description'])
@validsign
@validcall(2048)
def modify_tag():
    t = Tag.get_or_create(g.data['name'])
    t.org = g.data['org']
    t.description = g.data['description']
    t.save_changes()
    return trueReturn()

@handle_error
@tag_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['name'])
@validsign
@validcall(2048)
def remove_tag():
    t = Tag.objects(g.data['name'])
    if not t: return falseReturn(msg='无此标签')
    t.delete()
    return trueReturn()

@handle_error
@tag_blueprint.route('/chvis', methods=['POST'])
@verify_params(params=['visible'])
@validsign
@validcall(2048)
def chvis_tag():
    t = Tag.objects(g.data['name'])
    t.visible = g.data['visible']
    t.save()
    return trueReturn()

@handle_error
@tag_blueprint.route('/info', methods=['POST'])
@verify_params(params=['name'])
@validsign
@validcall(2048)
def info_tag():
    t = Tag.objects(g.data['name']).first()
    if not t: return falseReturn(msg='无此标签')
    return trueReturn(t.get_base_info())

@handle_error
@tag_blueprint.route('/ls', methods=['GET'])
@validsign
@validcall(2048)
def ls_tag():
    return trueReturn({'tags':[i.get_base_info() for i in Tag.objects()]})
