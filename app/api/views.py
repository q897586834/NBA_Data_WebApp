# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from . import api
from ..models import Users, Team, Team_Data, Attribute_Type, Coach, Coach_Data, Player, Player_Data, Player_Contract
from ..utils import season_dict, seasons, load_player_data_json, load_nutrient_data_json
from datatables import ColumnDT, DataTables
from .. import db
from sqlalchemy import and_


# 带prefix /api
@api.route('/json', methods=['GET', 'POST'])
def give_json_data():
    return '''{
    "data": [
        [
            "Tiger Nixon",
            "System Architect",
            "Edinburgh",
            "5421",
            "2011\/04\/25",
            "$320,800"
        ],
        [
            "Garrett Winters",
            "Accountant",
            "Tokyo",
            "8422",
            "2011\/07\/25",
            "$170,750"
        ]
    ]
}'''



#
#
#    API for Player Table
#
#

@api.route('/info/player', methods=['GET', 'POST'])
def player_info_table():
    columns = [
        ColumnDT(Player.player_name),
        ColumnDT(Player.year_start),
        ColumnDT(Player.year_end),
        ColumnDT(Player.position),
        ColumnDT(Player.height),
        ColumnDT(Player.weight),
        ColumnDT(Player.birth_year),
        ColumnDT(Player.college)
    ]

    # print(request.args)    # GET方法从args获取参数
    # print(request.form)    # POST方法从form获取参数
    # request.values    # 获取所有参数

    if request.method == 'POST':
        player_name = request.form.get('player_name')
        # season = request.form.get('season')
        # team_name = request.args.get('team_name')

        query = db.session.query().select_from(Player).filter(Player.player_name == player_name)

    # params = request.args.to_dict()    # GET方法 
    params = request.form.to_dict()    # POST方法
    rowTable = DataTables(params, query, columns)

    return jsonify(rowTable.output_result())

@api.route('/data/player', methods=['GET', 'POST'])
def player_data_table():
    columns = [
        ColumnDT(Player_Data.season),
        ColumnDT(Team.team_name),
        ColumnDT(Player_Data.attri_value),
        ColumnDT(Attribute_Type.attri_name)
    ]

    if request.method == 'POST':
        player_name = request.form.get('player_name')
        season = season_dict[request.form.get('season')]

        if season == '00--99':
            query = db.session.query().select_from(Team, Player_Data, Attribute_Type, Player).filter(
                and_(Team.team_id == Player_Data.team_id, 
                     Player_Data.attri_id == Attribute_Type.attri_id, 
                     Player.player_id == Player_Data.player_id,
                     Player.player_name == player_name))
        else:
            query = db.session.query().select_from(Team, Player_Data, Attribute_Type, Player).filter(
                    and_(Team.team_id == Player_Data.team_id, 
                     Player_Data.attri_id == Attribute_Type.attri_id, 
                     Player.player_id == Player_Data.player_id,
                     Player.player_name == player_name, 
                     Player_Data.season == season))

    params = request.form.to_dict()
    rowTable = DataTables(params, query, columns)
    
    return jsonify(rowTable.output_result())


#
#
#   Player_Data数据表改，增，删的API
#
#
@api.route('/data/player/edit', methods=['GET', 'POST'])
def player_data_table_edit():
    if current_user.role_id != 3:
        return jsonify({'status': 'fail'})

    if request.method == 'POST':
        player_name = request.form.get('player_name')
        season = request.form.get('season')
        team_name = request.form.get('team_name')
        attri_value = request.form.get('attri_value')
        attri_name = request.form.get('attri_name')
        
        query1 = db.session.query(Player).filter_by(player_name=player_name)
        player_id = query1.all()[0].player_id
        query2 = db.session.query(Attribute_Type).filter_by(attri_name=attri_name)
        attri_id = query2.all()[0].attri_id
        query3 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query3.all()[0].team_id

        player_data = Player_Data.query.filter(and_(Player_Data.player_id == player_id,
                                       Player_Data.team_id == team_id, 
                                       Player_Data.season == season,
                                       Player_Data.attri_id == attri_id)).first()
        player_data.attri_value = attri_value
        db.session.commit()
        # db.session.add(Team_Data(team_name, season, attri_value, attri_name))
        # db.session.commit()
    return jsonify({})

@api.route('/data/player/add', methods=['GET', 'POST'])
def player_data_table_add():
    if current_user.role_id != 3:
        return jsonify({'status': 'fail'})

    if request.method == 'POST':
        player_name = request.form.get('player_name')
        season = request.form.get('season')
        team_name = request.form.get('team_name')
        attri_value = request.form.get('attri_value')
        attri_name = request.form.get('attri_name')
        
        query1 = db.session.query(Player).filter_by(player_name=player_name)
        player_id = query1.all()[0].player_id
        query2 = db.session.query(Attribute_Type).filter_by(attri_name=attri_name)
        attri_id = query2.all()[0].attri_id
        query3 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query3.all()[0].team_id

        player_data = Player_Data(player_id, season, team_id, attri_value, attri_id)
        db.session.add(player_data)
        db.session.commit()

    return jsonify({})

@api.route('/data/player/delete', methods=['GET', 'POST'])
def player_data_table_delete():
    if current_user.role_id != 3:
        return jsonify({'status': 'fail'})

    if request.method == 'POST':
        player_name = request.form.get('player_name')
        season = request.form.get('season')
        team_name = request.form.get('team_name')
        attri_name = request.form.get('attri_name')
        
        query1 = db.session.query(Player).filter_by(player_name=player_name)
        player_id = query1.all()[0].player_id
        query2 = db.session.query(Attribute_Type).filter_by(attri_name=attri_name)
        attri_id = query2.all()[0].attri_id
        query3 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query3.all()[0].team_id

        Player_Data.query.filter(and_(Player_Data.player_id == player_id, 
                                      Player_Data.team_id == team_id, 
                                      Player_Data.season == season,
                                      Player_Data.attri_id == attri_id)).delete()
        db.session.commit()

    return jsonify({})





@api.route('/contract/player', methods=['GET', 'POST'])
def player_contract_table():
    columns = [
        ColumnDT(Player.player_name),
        ColumnDT(Player_Contract.season),
        ColumnDT(Team.team_name),
        ColumnDT(Player_Contract.salary)
    ]

    if request.method == 'POST':
        player_name = request.form.get('player_name')
        team_name = request.form.get('team_name')
        season = season_dict[request.form.get('season')]

        if season == '00--99':
            query = db.session.query().select_from(Player, Team, Player_Contract).filter(
                and_(Player.player_id == Player_Contract.player_id,
                     Team.team_id == Player_Contract.team_id,
                     Player.player_name == player_name))
        else:
            query = db.session.query().select_from(Player, Team, Player_Contract).filter(
                and_(Player.player_id == Player_Contract.player_id,
                     Team.team_id == Player_Contract.team_id,
                     Player_Contract.season == season,
                     Player.player_name == player_name))

    params = request.form.to_dict()
    rowTable = DataTables(params, query, columns)

    return jsonify(rowTable.output_result())


#
#
#   Player_Contract数据表改，增，删的API
#
#
@api.route('/contract/player/edit', methods=['GET', 'POST'])
def player_contract_table_edit():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        team_name = request.form.get('team_name')
        season = request.form.get('season')
        salary = request.form.get('salary')
        
        query1 = db.session.query(Player).filter_by(player_name=player_name)
        player_id = query1.all()[0].player_id
        query2 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query2.all()[0].team_id

        player_contract = Player_Contract.query.filter(and_(Player_Contract.player_id == player_id,
                                       Player_Contract.team_id == team_id, 
                                       Player_Contract.season == season)).first()
        player_contract.salary = salary
        db.session.commit()

    return jsonify({})

@api.route('/contract/player/add', methods=['GET', 'POST'])
def player_contract_table_add():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        team_name = request.form.get('team_name')
        season = request.form.get('season')
        salary = request.form.get('salary')
        
        query1 = db.session.query(Player).filter_by(player_name=player_name)
        player_id = query1.all()[0].player_id
        query2 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query2.all()[0].team_id

        player_contract = Player_Contract(player_id, team_id, season, salary)
        db.session.add(player_contract)
        db.session.commit()

    return jsonify({})

@api.route('/contract/player/delete', methods=['GET', 'POST'])
def player_contract_table_delete():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        team_name = request.form.get('team_name')
        season = request.form.get('season')
        
        query1 = db.session.query(Player).filter_by(player_name=player_name)
        player_id = query1.all()[0].player_id
        query2 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query2.all()[0].team_id

        Player_Contract.query.filter(and_(Player_Contract.player_id == player_id, 
                                      Player_Contract.team_id == team_id, 
                                      Player_Contract.season == season)).delete()
        db.session.commit()

    return jsonify({})




@api.route('/User_Info', methods=['GET', 'POST'])
def api_User_Info():
    

    columns = [
        ColumnDT(Users.id),
        ColumnDT(Users.name),
        ColumnDT(Users.role_id)
    ]

    query = db.session.query().select_from(Users).filter(Users.role_id == 1)
    query2 = db.session.query(Users).filter_by(role_id=1)
    # query = db.session.query().select_from(Team).filter(Team.team_name == 'OKC')
    # query = Users.query.filter_by(Users.role_id == 1).order_by(Users.id)
    # 需要draw, length, start三个参数，来正常运行DataTable包
    params = request.args.to_dict()
    rowTable = DataTables(params, query, columns)
    # print(query.scalar())
    # print(query2)
    # print(query2.all())
    # print(query2.all()[3].name)
    # print(rowTable.output_result()['data'])
    # print((Users.query.filter(Users.name == 'tuige')).all())

    return jsonify(rowTable.output_result())
    # return 'abc'

def update_data_user():
    pass

@api.route('/info/datatable', methods=['GET', 'POST'])
def change_data_table():
    if request.method == 'POST':
        return jsonify({"table": "User_Info"})
    return jsonify({"table": "data"})    



#
#
#    API for Team Table
#
#

@api.route('/info/team', methods=['GET', 'POST'])
def team_data_table1():
    columns = [
        ColumnDT(Team.team_name),
        ColumnDT(Team.team_city),
        ColumnDT(Team.team_year)
    ]

    # print(request.args)    # GET方法从args获取参数
    # print(request.form)    # POST方法从form获取参数
    # request.values    # 获取所有参数

    if request.method == 'POST':
        team_name = request.form.get('team_name')
        # season = request.form.get('season')
        # team_name = request.args.get('team_name')

        query = db.session.query().select_from(Team).filter(Team.team_name == team_name)

    # params = request.args.to_dict()    # GET方法 
    params = request.form.to_dict()    # POST方法
    rowTable = DataTables(params, query, columns)

    return jsonify(rowTable.output_result())

@api.route('/data/team', methods=['GET', 'POST'])
def team_data_table2():
    columns = [
        ColumnDT(Team.team_name),
        ColumnDT(Team_Data.season),
        ColumnDT(Team_Data.attri_value),
        ColumnDT(Attribute_Type.attri_name)
    ]

    if request.method == 'POST':
        team_name = request.form.get('team_name')
        season = season_dict[request.form.get('season')]

        if season == '00--99':
            query = db.session.query().select_from(Team, Team_Data, Attribute_Type).filter(
                and_(Team.team_id == Team_Data.team_id, 
                     Team_Data.attri_id == Attribute_Type.attri_id, 
                     Team.team_name == team_name))
        else:
            query = db.session.query().select_from(Team, Team_Data, Attribute_Type).filter(
                    and_(Team.team_id == Team_Data.team_id, 
                    Team_Data.attri_id == Attribute_Type.attri_id, 
                    Team.team_name == team_name, Team_Data.season == season))
    else:
        query = db.session.query().select_from(Team, Team_Data, Attribute_Type).filter(
                and_(Team.team_id == Team_Data.team_id, 
                     Team_Data.attri_id == Attribute_Type.attri_id, 
                     Team.team_name == 'OKC'))
    params = request.form.to_dict()
    rowTable = DataTables(params, query, columns)
    
    return jsonify(rowTable.output_result())

#
#
#   Team_Data数据表改，增，删的API
#
#
@api.route('/data/team/edit', methods=['GET', 'POST'])
def team_data_table_edit():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        season = request.form.get('season')
        attri_value = request.form.get('attri_value')
        attri_name = request.form.get('attri_name')

        query1 = db.session.query(Attribute_Type).filter_by(attri_name=attri_name)
        attri_id = query1.all()[0].attri_id
        query2 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query2.all()[0].team_id

        team_data = Team_Data.query.filter(and_(Team_Data.team_id == team_id, Team_Data.season == season,
                                       Team_Data.attri_id == attri_id)).first()
        team_data.attri_value = attri_value
        db.session.commit()
        # db.session.add(Team_Data(team_name, season, attri_value, attri_name))
        # db.session.commit()
    return jsonify({})

@api.route('/data/team/add', methods=['GET', 'POST'])
def team_data_table_add():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        season = request.form.get('season')
        attri_value = request.form.get('attri_value')
        attri_name = request.form.get('attri_name')

        query1 = db.session.query(Attribute_Type).filter_by(attri_name=attri_name)
        attri_id = query1.all()[0].attri_id
        query2 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query2.all()[0].team_id

        team_data = Team_Data(team_id, season, attri_value, attri_id)
        db.session.add(team_data)
        db.session.commit()

    return jsonify({})

@api.route('/data/team/delete', methods=['GET', 'POST'])
def team_data_table_delete():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        season = request.form.get('season')
        attri_name = request.form.get('attri_name')

        query1 = db.session.query(Attribute_Type).filter_by(attri_name=attri_name)
        attri_id = query1.all()[0].attri_id
        query2 = db.session.query(Team).filter_by(team_name=team_name)
        team_id = query2.all()[0].team_id

        Team_Data.query.filter(and_(Team_Data.team_id == team_id, Team_Data.season == season,
                                       Team_Data.attri_id == attri_id)).delete()
        db.session.commit()

    return jsonify({})



#
#
#    API for Coach Table
#
#

# @api.route('/info/coach', methods=['GET', 'POST'])
# def coach_info_table():
#     pass

@api.route('/data/coach', methods=['GET', 'POST'])
def coach_data_table():
    columns = [
        ColumnDT(Coach.coach_name),
        ColumnDT(Coach_Data.season),
        ColumnDT(Coach_Data.win),
        ColumnDT(Coach_Data.loss)
    ]

    if request.method == 'POST':
        coach_name = request.form.get('coach_name')
        season = season_dict[request.form.get('season')]
        if season == '00--99':
            query = db.session.query().select_from(Coach, Coach_Data).filter(
                    and_(Coach.coach_id == Coach_Data.coach_id, 
                         Coach.coach_name == coach_name))
        else:
            query = db.session.query().select_from(Coach, Coach_Data).filter(
                    and_(Coach.coach_id == Coach_Data.coach_id, 
                         Coach.coach_name == coach_name),
                         Coach_Data.season == season)

    params = request.form.to_dict()
    rowTable = DataTables(params, query, columns)

    return jsonify(rowTable.output_result())


#
#
#   Coach_Data数据表改，增，删的API
#
#
@api.route('/data/coach/edit', methods=['GET', 'POST'])
def coach_data_table_edit():
    if request.method == 'POST':
        coach_name = request.form.get('coach_name')
        season = request.form.get('season')
        win = request.form.get('win')
        loss = request.form.get('loss')

        query1 = db.session.query(Coach).filter_by(coach_name=coach_name)
        coach_id = query1.all()[0].coach_id

        coach_data = Coach_Data.query.filter(and_(Coach_Data.coach_id == coach_id, 
                                                 Coach_Data.season == season)).first()
        coach_data.win = int(win)
        coach_data.loss = int(loss)
        db.session.commit()

    return jsonify({})

@api.route('/data/coach/add', methods=['GET', 'POST'])
def coach_data_table_add():
    if request.method == 'POST':
        coach_name = request.form.get('coach_name')
        season = request.form.get('season')
        win = request.form.get('win')
        loss = request.form.get('loss')
        
        query1 = db.session.query(Coach).filter_by(coach_name=coach_name)
        coach_id = query1.all()[0].coach_id

        coach_data = Coach_Data(coach_id, season, int(win), int(loss))
        db.session.add(coach_data)
        db.session.commit()

    return jsonify({})

@api.route('/data/coach/delete', methods=['GET', 'POST'])
def coach_data_table_delete():
    if request.method == 'POST':
        coach_name = request.form.get('coach_name')
        season = request.form.get('season')

        query1 = db.session.query(Coach).filter_by(coach_name=coach_name)
        coach_id = query1.all()[0].coach_id

        Coach_Data.query.filter(and_(Coach_Data.coach_id == coach_id, 
                                     Coach_Data.season == season)).delete()
        db.session.commit()

    return jsonify({})


#
#
#    API for User & Role Table
#
#



#
#
#    API for ECharts
#
#

@api.route('/charts/nutrient')
def nutrient_json():
    # print(json_dict)
    json_dict = load_nutrient_data_json()
    return jsonify(json_dict)

@api.route('/charts/nba', methods=['GET', 'POST'])
def nba_player_data_json():
    json_list = load_player_data_json()
    return jsonify(json_list)
    # if request.method == 'POST':
    #     season = season_dict[request.form.get('season')]
    #     index = seasons.index(season)
    # else:
    #     index = 0    # 06/07赛季
    # return jsonify(json_list[index])
