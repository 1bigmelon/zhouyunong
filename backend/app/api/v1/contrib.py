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
from app.models.Article import Contrib, Tag, Div
from app.util.auth import generate_jwt, verify_jwt, general_before_request

contrib_blueprint = Blueprint('contrib', __name__, url_prefix='/contrib')

@contrib_blueprint.before_request
def before_request():
    return general_before_request()

@handle_error
@contrib_blueprint.route('/new', methods=['POST'])
@verify_params(params=['author', 'title', 'email', 'content', 'org'])
def new_contrib():
    o = Org.objects(id=g.data['org']).first()
    c = Contrib(
        author=g.data['author'],
        title=g.data['title'],
        email=g.data['email'],
        content=g.data['content'],
        org=o,
        create_time=datetime.datetime.now()
    ).save_changes()
    return trueReturn(c.get_base_info())

@handle_error
@contrib_blueprint.route('/deny', methods=['POST'])
@verify_params(params=['id'])
@validsign
def deny_contrib():
    c = Contrib.objects(id=g.data['id']).first()
    if not c: return falseReturn(msg='投稿不存在')
    c.status = '未通过'
    c.save_changes()
    return trueReturn()

@handle_error
@contrib_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def remove_contrib():
    c = Contrib.objects(id=g.data['id']).first()
    if not c: return falseReturn(msg='投稿不存在')
    c.delete()
    return trueReturn()

@handle_error
@contrib_blueprint.route('/accept', methods=['POST'])
@verify_params(params=['id', 'div', 'tags'])
@validsign
def accept_contrib():
    c = Contrib.objects(id=g.data['id']).first()
    if not c: return falseReturn(msg='投稿不存在')
    if c.status == '未通过': return falseReturn(msg='不能操作未通过的投稿')
    t = []
    for i in g.data['tags']:
        t.append(Tag.objects(id=i).first())
    d = Div.objects(id=g.data['div']).first()
    c.convert_to_article(d, t)
    return trueReturn()

@handle_error
@contrib_blueprint.route('/modify', methods=['POST'])
@verify_params(params=['id'])
@validsign
def chinfo_contrib():
    c = Contrib.objects(id=g.data['id']).first()
    modifiable = {
        'author', 'title', 'email', 'content', 'org'
    }
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            if k == 'org':
                modify_keys['org'] = Org.objects(id=v).first()
            else:
                modify_keys[k] = v

    c.modify(**modify_keys)
    c.save_changes()
    return trueReturn()

@handle_error
@contrib_blueprint.route('/search', methods=['POST'])
@validsign
def search_contrib():
    sd = {
        'author', 'title', 'status', 'content'
    }
    begin = datetime.datetime.min
    end = datetime.datetime.max
    if 'time' in g.data:
        begin, end = [datetime.datetime.fromtimestamp(float(i)) for i in g.data['time'].split('-')]
    
    ks = {}
    for k, v in g.data.items():
        if k in sd:
            if k == 'author':
                ks['author__icontains']=v
            elif k == 'title':
                ks['title__icontains']=v
            elif k == 'content':
                ks['content__icontains']=v
            else:
                ks[k] = v

    c = Contrib.objects(**ks)
    return trueReturn({'contribs':[i.get_base_info() for i in c if begin <= i.create_time <= end]})


@handle_error
@contrib_blueprint.route('/ls', methods=['GET'])
@validsign
def ls_contrib():
    c = Contrib.objects()
    new_ctr = 0
    for i in c:
        if i.create_time.timetuple() >= datetime.datetime.now().date().timetuple():
            new_ctr += 1
    return trueReturn({
        'contribs':[i.get_base_info() for i in c],
        'new': new_ctr
    })

@handle_error
@contrib_blueprint.route('/info', methods=['POST'])
@verify_params(params=['id'])
@validsign
def info_contrib():
    c = Contrib.objects(id=g.data['id']).first()
    if not c: return falseReturn(msg='无此投稿')
    return trueReturn(c.get_all_info())