from bs4 import BeautifulSoup
import requests 
import os
import json
import re

url = "https://students.tw/5599/"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C hrome/105.0.0.0 Safari/537.36"}

res = requests.get(url , headers = headers)
soup = BeautifulSoup(res.text,"html.parser")

  
title = soup.find_all("p")


date=[]
def date(ary):
    for i in title:
        if str(i.text)[:5] =="➤活動日期":
            date.append(str(i.text)[6:])
    date[17]="2"+date[17]
 
print(date[17])
