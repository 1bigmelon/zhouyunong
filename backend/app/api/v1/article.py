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

from app.util.auth import generate_jwt, verify_jwt
from app.util.sheet import sheet

article_blueprint = Blueprint('article', __name__, url_prefix='/article')

@article_blueprint.before_request
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
@article_blueprint.route('/new', methods=['POST'])
@verify_params(params=[
    'title',
    'div',
    'author',
    'email'
])
@validsign
def new_article():
    article = Article(
        title=g.data['title'],
        source=g.data.get('source', ''),
        email=g.data['email'],
        author=g.data['author']
    )
    article.tags = [Tag.objects(name=i).first() for i in g.data['tags']]
    article.div = Div.objects(name=g.data['div'])
    article.create_time = datetime.datetime.now()
    article.save_changes()
    return trueReturn()

@handle_error
@article_blueprint.route('/remove', methods=['POST'])
@verify_params(params=['id'])
@validsign
def remove_article():
    Article.objects(id=g.datap['id']).remove()
    return trueReturn()

@handle_error
@article_blueprint.route('/edit', methods=['POST'])
@verify_params(params=['id', 'permission', 'functions'])
@validsign
@validcall
def edit_article():
    if g.user.restrict_permission(g.data['permission']):
        if g.user.restrict_functions(g.data['functions']):
            Role.get_by_id(g.data['id']).modify_permission(g.data['permission'])
            Role.get_by_id(g.data['id']).modify_functions(g.data['functions'])
            return trueReturn()
        else:
            return falseReturn(msg='您无法为角色分配自己没有的权能')
    else:
        return falseReturn(msg='您无法为角色分配不小于自身的权限')


@handle_error
@article_blueprint.route('/ls', methods=['GET'])
@validsign
def ls_article():
    return trueReturn({"articles":[i.get_base_info() for i in Article.objects()]})