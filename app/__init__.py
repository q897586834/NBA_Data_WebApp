# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
# from .models import Users

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection='strong'
# 当未登录的用户尝试访问一个 login_required 装饰的视图，Flask-Login会闪现一条消息并且重定向到登录视图
login_manager.login_view='auth.login'



def create_app(config_name):
    # 程序的工厂函数
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 导入auth文件夹中__init__.py定义的Blueprint，并注册Blueprint
    from .auth import auth as auth_blueprint     
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

