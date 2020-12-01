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
from app.models.Article import Article, Tag, Div
from app.models.Org import Org
from app.util.auth import generate_jwt, verify_jwt, general_before_request

article_blueprint = Blueprint('article', __name__, url_prefix='/article')

@article_blueprint.before_request
def before_request():
    general_before_request()

@handle_error
@article_blueprint.route('/new', methods=['POST'])
@verify_params(params=[
    'title',
    'div',
    'author',
    'div',
    'tags',
    'email',
    'content'
])
@validsign
def new_article():
    article = Article(
        title=g.data['title'],
        content=g.data['content'],
        email=g.data['email'],
        author=g.data['author']
    )
    article.tags = [Tag.objects(id=i).first() for i in g.data['tags']]
    article.div = Div.objects(id=g.data['div'])
    if 'org' in g.data:
        article.org = Org.objects(id=g.data['org']).first()
    article.create_time = datetime.datetime.now()
    article.save_changes()
    return trueReturn()

@handle_error
@article_blueprint.route('/modify', methods=['POST'])
@verify_params(params=['id'])
@validsign
@validcall(0x1110)
def modify_article():
    a = Article.objects(id=g.data['id']).first()
    modifiable = {
        'title', 'org', 'content',
        'div', 'author', 'email', 'pin', 'tags'
    }
    modify_keys = {}
    for k, v in g.data.items():
        if k in modifiable:
            if k == 'org':
                modify_keys[k] = Org.objects(id=v).first()
            elif k == 'div':
                modify_keys[k] = Div.objects(id=v).first()
            elif k == 'tags':
                modify_keys[k] = [Tag.objects(id=i).first() for i in v]
            else:
                modify_keys[k] = v
    a.modify(**modify_keys)
    a.save_changes()
    return trueReturn()

@handle_error
@article_blueprint.route('/forward', methods=['POST'])
@verify_params(params=['id'])
@validsign
def forward_article():
    a = Article.objects(id=g.data['id']).first()
    if a.status == '待一审' and g.user.authority & 0x10:
        a.status = '待二审'
    elif a.status == '待二审' and g.user.authority & 0x100:
        a.status = '待终审'
    elif a.status == '待终审' and g.user.authority & 0x1000:
        a.status = '待发布'
    elif a.status == '待发布' and g.user.authority & 0x1000:
        a.status = '已发布'
    else:
        return falseReturn(msg='您没有权限执行此操作')
    a.save_changes()
    return trueReturn()

@handle_error
@article_blueprint.route('/revoke', methods=['POST'])
@verify_params(params=['id'])
@validsign
def revoke_article():
    a = Article.objects(id=g.data['id']).first()

    if a.status == '待二审' and g.user.authority & 0x100:
        a.status = '待一审'
    elif a.status == '待终审' and g.user.authority & 0x1000:
        a.status = '待二审'
    elif a.status == '待发布' and g.user.authority & 0x1000:
        a.status = '待终审'
    elif a.status == '已发布' and g.user.authority & 0x1000:
        a.status = '待发布'
    else:
        return falseReturn(msg='您没有权限执行此操作')
    a.save_changes()
    return trueReturn()

@handle_error
@article_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
def remove_article():
    a = Article.objects(id=g.data['id']).first()
    if a.status != '储存库':
        return falseReturn(msg='您只能删除储存库中的文章')
    a.delete()
    return trueReturn()

@handle_error
@article_blueprint.route('/stash', methods=['POST'])
@verify_params(params=['id'])
@validsign
def stash_article():
    a = Article.objects(id=g.data['id']).first()
    if a.status != '已发布':
        a.status = '储存库'
    else:
        return falseReturn(msg='您不能直接移除已发布文章')
    a.save_changes()
    return trueReturn()

@handle_error
@article_blueprint.route('/recover', methods=['POST'])
@verify_params(params=['id'])
@validsign
def recover_article():
    a = Article.objects(id=g.data['id']).first()
    if a.status == '储存库':
        a.status = '待一审'
    else:
        return falseReturn(msg='文章不在储存库，无需回复')
    a.save_changes()
    return trueReturn()

@handle_error
@article_blueprint.route('/ls', methods=['GET'])
@validsign
def ls_article():
    return trueReturn({"articles":[i.get_base_info() for i in Article.objects()]})

@handle_error
@article_blueprint.route('/search', methods=['POST'])
@validsign
def search_article():
    sd = {
        'title', 'org', 'content',
        'div', 'author', 'email', 'pin', 'tags'
    }
    ks = {}
    for k, v in g.data.items():
        if k in sd:
            if k == 'title':
                ks['title__icontains'] = v
            elif k == 'org':
                ks['org'] = Org.objects(name=v).first()
            elif k == 'content':
                ks['content__icontains'] = v
            elif k == 'tags':
                ks['tags__in'] = [Tag.objects(id=i).first() for i in v]
            else:
                ks[k] = v
    return trueReturn({
        "articles":[
            i.get_base_info() for i in Article.objects(**ks)
        ]
    })

@handle_error
@article_blueprint.route('/show', methods=['POST'])
def show_article():
    sd = {
        'title', 'org', 'content',
        'div', 'author', 'pin', 'tags'
    }
    ks = {}
    for k, v in g.data.items():
        if k in sd:
            if k == 'title':
                ks['title__icontains'] = v
            elif k == 'org':
                ks['org'] = Org.objects(name=v).first()
            elif k == 'content':
                ks['content__icontains'] = v
            elif k == 'tags':
                ks['tags__in'] = [Tag.objects(id=i).first() for i in v]
            else:
                ks[k] = v
    return trueReturn({
        "articles":[
            i.get_base_info() for i in Article.search_visibles(**ks)
        ]
    })