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

titles = soup.find_all("h3",class_="ftwp-heading")

image = []
for title in titles:
    try:
        images = title.find_next_sibling("figure")
        image.append(images.source['srcset'])
    except TypeError as e:
        image.append("")
    
print(len(image))
