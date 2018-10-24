# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import Users
# from ..email import send_email
from . import auth
from .forms import Login_Form, Register_Form
from flask_login import login_user, logout_user, login_required, current_user



# @auth.route('/', methods=['GET', 'POST'])
# def index():
#     # form = NameForm()
#     form = Login_Form()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#             if current_app.config['FLASKY_ADMIN']:
#                 send_email(current_app.config['FLASKY_ADMIN'], 'New User',
#                            'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         return redirect(url_for('.index'))    # url_for的用法主要加命名空间（即蓝本名），省略写作.，跨蓝本不行
#     return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False))


@auth.route('/login',methods=['GET','POST'])
# @auth.route('/login/',methods=['GET','POST'])
def login():
    form=Login_Form()
    # 直接访问login的时候form表单是没有值的，检查是否是POST请求（不用request.method==POST）且是否有效
    if form.validate_on_submit():
        # 这里也就是数据库中不能有重名情况        
        user=Users.query.filter_by(name=form.name.data).first()
        if user is not  None and user.pwd==form.pwd.data:
            login_user(user)
            flash('登录成功')
            
            # # 验证user对于next的权限，避免遭到重定向攻击
            # next = flask.request.args.get('next')
            # if non next_is_valid(next):
            #     return flask.abort(400)

            # return render_template('ok.html',name=form.name.data)
            # return render_template('index.html', name=form.name.data)
            return redirect(url_for('main.home_page'))
        else:
            flash('用户或密码错误')
            return render_template('login.html',form=form)

    return render_template('login.html', form=form)    # 解决不显示login的问题

#用户登出
@auth.route('/logout')
@login_required    # 即需要用户登录的视图
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
    form=Register_Form()
    if form.validate_on_submit():
        user=Users(name=form.name.data,pwd=form.pwd.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('main.index'))
    return render_template('register.html',form=form)
