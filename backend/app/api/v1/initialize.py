import datetime
import hashlib
import json
import traceback
import os

import requests
from flask import Blueprint
from flask import current_app as flaskapp
from flask import g, jsonify, request
from mongoengine.queryset.visitor import Q

from app.api import handle_error, validsign, verify_params
from app.common.result import falseReturn, trueReturn
from app.models.User import User

from app import db

initialize_blueprint = Blueprint('initialize', __name__, url_prefix='/initialize')

@initialize_blueprint.route('/pull', methods=['GET'])
def git_pull():
    os.system('git pull')
    with open('reload','w') as f:
        pass
    return trueReturn()
