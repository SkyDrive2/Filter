import os
import requests
import json

HOST = "http://36.236.61.181:5044/api/activity"

json_file_name = 'filter_after'
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
with open(os.path.join(parent_path, json_file_name), "r") as json_file:
    json_data = json.load(json_file)
    r = requests.post(HOST, data=json_data)
    if r.ok == 200:
        print("上傳成功")
    else:
        print