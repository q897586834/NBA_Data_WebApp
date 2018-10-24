from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views, errors    # 避免循环导入
