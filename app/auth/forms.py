# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Required, Length, Regexp, EqualTo


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

#登录表单
class Login_Form(FlaskForm):
    name=StringField('name',validators=[Required()])
    pwd=PasswordField('pwd',validators=[Required()])
    submit=SubmitField('Login in')


#注册表单
class Register_Form(FlaskForm):
	# name只能为字母开头，由字母和数字组成
    name=StringField('name',validators=[Required(), Length(1, 32),
    	             Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
    	             'Usernames must have only letters, numbers, dots or underscores')])
    # 密码输入两次，EqualTo验证
    pwd=PasswordField('pwd',validators=[Required(), Length(1, 32),
    	              EqualTo('pwd2', message='Passwords must match')])
    pwd2=PasswordField('Confirm pwd', validators=[Required()])
    submit=SubmitField('register')

