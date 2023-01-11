import requests
from bs4 import BeautifulSoup
import os
import json
import datetime
import itertools
now = datetime.datetime.now()
date_t = "上次更新時間為: " + str(now)
with open("C:\\Users\\aazz1\\OneDrive\\桌面\\store_code\\Filter\\re_filter_tool\\daily_crawler\\camping\\test.txt", "w", encoding="utf-8") as writefile:
    writefile.write(date_t)
activities = []
header ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
for i in itertools.count(start = 1):
    o_url = f"https://www.g9cip.com/category/activity/page/{i}/"
    res = res = requests.get(o_url, header)
    soup = BeautifulSoup(res.text, "html.parser")
    
    if soup.find("body", class_ = "error404 wp-custom-logo elementor-default elementor-kit-7 e--ua-blink e--ua-chrome e--ua-webkit"):
        print(o_url)
        break