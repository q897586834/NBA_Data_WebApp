# -*- coding: utf-8 -*-

import json
from flask import render_template, request, jsonify
from flask_login import login_required
from . import main
# 查询数据时需要提供的表单
from .forms import Team_Table_Form
from ..utils import scatter3d, scatter2d



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/index')
def l_index():
    return render_template('index.html')

# Home Page
@main.route('/home')
@login_required
def home_page():
    return render_template('index4.html')



#
#
#    Pages for Data Table
#
#

# 数据表页面，进行增删改查的操作
@main.route('/tables/data', methods=['POST', 'GET'])
@login_required
def player_data_table():
    return render_template('tables/data.html')

@main.route('/charts/chart', methods=['POST', 'GET'])
@login_required
def chart():
    return render_template('charts/chart.html')

def prediction():
    pass



#
#
#    Pages for Chart
#
#

@main.route('/charts/3dchart')
def hello():
    # s3d = scatter3d()
    s2d = scatter2d()
    # return render_template(
    #     "pyecharts.html",
    #     myechart=s3d.render_embed(),
    #     host=REMOTE_HOST,
    #     script_list=s3d.get_js_dependencies(),
    # )
    return render_template(
        "charts/chart_base.html",
        myechart=s2d.render_embed())

@main.route('/charts/scatter3d')
def nutrient_data_scatter_3d():
    return render_template('charts/scatter3d.html')

@main.route('/charts/player_data')
def player_data_scatter_3d():
    # return render_template('charts/scatter3d_nba.html')
    return render_template('charts/chart_scatter3d_season.html')
