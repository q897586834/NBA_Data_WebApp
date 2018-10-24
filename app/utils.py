# -*- coding: utf-8 -*-

import random
import json
import os, sys
from pyecharts import Scatter3D, Scatter



#
#
#    Global Variables
#
#

season_dict = {
     '06/07': '06--07',
     '07/08': '07--08',
     '08/09': '08--09',
     '09/10': '09--10',
     '10/11': '10--11',
     '11/12': '11--12',
     '12/13': '12--13',
     '13/14': '13--14',
     '14/15': '14--15',
     '15/16': '15--16',
     '16/17': '16--17',
     'all_seasons': '00--99',
     'no_season_selected': '06--07'
}

__in_filename__ = '/Users/wu/python/data_analysis/NBA/avg_new.csv'
__out_filename__ = '/Users/wu/python/flask/NBA_DB_System/app/templates/charts/json/player_data_'
    
seasons = [
    '06--07', '07--08', '08--09', '09--10', '10--11', 
    '11--12', '12--13', '13--14', '14--15', '15--16', '16--17'
]


#
#
#    Charts
#
#

def scatter3d():
    data = [generate_3d_random_point() for _ in range(3)]
    range_color = [
        "#313695",
        "#4575b4",
        "#74add1",
        "#abd9e9",
        "#e0f3f8",
        "#fee090",
        "#fdae61",
        "#f46d43",
        "#d73027",
        "#a50026",
    ]

    # mark_point_list = generate_3d_random_point_with_names(data)
    # scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
    scatter3D = Scatter3D("3D scattering plot demo without settings of width and height")
    scatter3D.add("", data, grid3d_width=200, grid3d_height=200, grid3d_depth=200,
         xaxis3d_name='Assist', yaxis3d_name='Rebound', zaxis3d_name='Point',
         is_visualmap=True, visual_range_color=range_color, visual_range=[0, 50])
    return scatter3D


def generate_3d_random_point():
    return [
        random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)
    ]

def generate_2d_random_point_with_names(data):
    ans = []
    for i in range(50):
        d = {}
        d['coord'] = data[i][0:2]
        d['name'] = "Point" + str(i)
        ans.append(d)

    return ans

def scatter2d():
    data = [generate_3d_random_point() for _ in range(50)]
    mark_point_list = generate_2d_random_point_with_names(data)

    x_list = [v[0] for v in data]
    y_list = [v[1] for v in data]
    extra_list = [v[2] for v in data]

    sc = Scatter("2D scattering plot demo with extra data")
    sc.add("", x_list, y_list, extra_data=extra_list, is_visualmap=True, visual_range=[0, 50],
        xaxis_name='Point', yaxis_name='Assist', visual_type='color', mark_point_symbolsize=35,
        mark_point=mark_point_list)
    return sc

def generate_one_axis_of_random_point(point_num, lowerbound, upperbound):
    return [random.randint(lowerbound, upperbound) for _ in range(point_num)]

def get_player_data_json():
    file = open(__in_filename__)
    data = file.readlines()[1:]

    for i in range(len(seasons)):
        all_data = []

        for line in data:
            new_line = line[:-1].split(',')
            if new_line[1] == seasons[i]:
                all_data.append(new_line)

        filename = __out_filename__ + seasons[i] + '.json'
        fr = open(filename, 'w')
        fr.seek(0, 0)

        fr.write(json.dumps(all_data))

def load_player_data_json():
    get_player_data_json()
    json_list = []

    for i in range(len(seasons)):
        filename = __out_filename__ + seasons[i] + '.json'
        with open(filename) as f2:
            json_dict2 = json.load(f2)
            json_list.append(json_dict2)

    return json_list

def load_nutrient_data_json():
    with open('/Users/wu/python/flask/NBA_DB_System/app/templates/charts/json/nutrients.json') as f1:
        json_dict1 = json.load(f1)
    return json_dict1
