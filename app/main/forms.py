# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields import core
from wtforms.validators import DataRequired, Required, Length, Regexp, EqualTo

class Team_Table_Form(FlaskForm):
    '''

         球队数据表查询表单

    '''
    team_name_field = StringField('team_name', validators=[Required()])
    season_field = StringField('season（输入例如：16/17）', validators=[Required()])
    submit = SubmitField('Submit')

    # c=StringField('c',validators=[Required()])
    # d=core.SelectMultipleField(
    #         label='d',
    #         choices=(
    #                 (1, 'aaa'),
    #                 (2, 'bbb'),
    #                 (3, 'ccc'),
    #                 (4, 'ddd')
    #             ),
    #         coerce=int
    #     )

class Player_Table_Form(FlaskForm):
    '''

        球员数据表查询表单

    '''
    player_name_field = StringField('player_name', validators=[Required()])
    year_start_field = StringField('year_start', validators=[Required()])
    birth_year_field = StringField('birth_year', validators=[Required()])
    submit = SubmitField('Submit')

class Coach_Table_Form(FlaskForm):
    '''

        教练数据查询表单

    '''
    coach_name_field = StringField('coach_name', validators=[Required()])
    season_field = StringField('season（输入例如：16/17）', validators=[Required()])
    submit = SubmitField('Submit')
