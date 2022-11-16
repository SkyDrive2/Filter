from bs4 import BeautifulSoup
import requests 
import os
import json
import re
import uuid


url = "https://students.tw/5599/"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) C hrome/105.0.0.0 Safari/537.36"}

res = requests.get(url , headers = headers)
soup = BeautifulSoup(res.text,"html.parser")

title = soup.find_all("h3",class_="ftwp-heading")
content = soup.find_all("p")

image_list = []
listA = []

it = soup.find_all("figure",class_ = 'wp-block-image size-full')
for i in it:
    for o in i :
        listA.append(o.source['srcset'])

print(len(listA))