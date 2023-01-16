import os
import requests
import json
import math

HOST = "http://36.236.28.96:5044/api/activity"


def activity_controller_async(activity_list):
    chop_group_num = 1
    finished_post = 0
    total_post = math.ceil(len(activity_list)/chop_group_num)

    for _ in range(total_post):
        result = post_activity_async(activity_list[0:chop_group_num])
        if result:
            finished_post += 1
        print(f'completed : {finished_post}/{total_post}', end='')
        del activity_list[0:chop_group_num]
        break

    print('\nall done!')


def post_activity_async(post_list):
    print(post_list)
    r = requests.post(HOST, json=post_list, timeout=5)
    print(r.status_code)
    if r.ok:
        return True
    else:
        return False


json_file_name = 'filter_after.json'
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
with open(os.path.join(parent_path, 're_filter_tool', json_file_name), "r", encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    activity_controller_async(json_data)
