import requests
import json

IP = "localhost"
PORT = "5000"
POST_URL = f"http://{IP}:{PORT}/api/activities"

with open("./re_filter_tool/filter_after.json", "r", encoding="utf-8") as openFile:
    JsonData = json.loads(openFile.read())
    tempList = []
    for index, post in enumerate(JsonData):
        if index % 3 == 0 and index != 0:
            requests.post(POST_URL, data=tempList)
            tempList.clear()
        tempList.append(post)
    if len(tempList) != 0:
        requests.post(POST_URL, data=tempList)
