import requests
from bs4 import BeautifulSoup
import json 
import os
url = "https://culture.tycg.gov.tw/home.jsp?id=93&parentpath=0,16&mcustomize=activityhot_view.jsp&dataserno=202212080001&aplistdn=ou=data,ou=activityhot,ou=chinese,ou=ap_root,o=tycg,c=tw&toolsflag=Y"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

res = requests.get(url,header)
soup = BeautifulSoup(res.text,"html.parser")

img_list = []
images = soup.find_all("div",class_ = "div_pic")
for image in images:
    print(image.a['href'])
    # img_list.append("https://culture.tycg.gov.tw/"+image.a['href'][1:])