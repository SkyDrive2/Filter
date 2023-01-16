import requests
from bs4 import BeautifulSoup
import itertools
import json

header ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

url = "https://www.g9cip.com/activity/exhibitions/%e5%98%89%e7%be%a9%e4%ba%ba%ef%bc%8e%e5%98%89%e7%be%a9%e4%ba%8b%e5%9c%a8%e5%9c%b0%e6%95%85%e4%ba%8b%e5%be%ae%e5%9e%8b%e5%b1%95/"
res = requests.get(url, headers = header)
soup = BeautifulSoup(res.text, "html.parser")
li = soup.select("body > div > section > div > div > div > section > div > div")
for i in li :
    if i.get("data-settings") == '{"background_background":"classic","_ob_bbad_is_stalker":"no","_ob_teleporter_use":false,"_ob_column_hoveranimator":"no","_ob_column_has_pseudo":"no"}':
        imgli = i.select("img")
        for j in imgli:
            print(j["data-src"])
    