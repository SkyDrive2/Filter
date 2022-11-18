from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

import time
import json
import os

url = "https://bhuntr.com/tw/competitions/?menu=true"

driver = webdriver.Chrome(executable_path = './chromedriver.exe')

driver.get(url)
driver.implicitly_wait(1000)

temp_height = 0
buttom_position = 8
while True:
    position = '//*[@id="bh-content"]/div/section/div/div/div/div[{}]/button'.format(buttom_position)
    try:
        driver.find_element("xpath",position).click()
        
    except AttributeError as e:
        break
    buttom_position+=24
    if buttom_position == 320:
        break
    time.sleep(4)


# time.sleep(10)
# print(driver.find_element('a').text())
url_list = []
title = []
s = driver.find_elements(By.TAG_NAME, "a")
for i in s:
    if i.text == "全部比賽":
        continue
    elif i.text == "設計比賽":
        continue
    elif i.text == "比賽":
        continue
    elif i.text == "影片比賽":
        continue
    elif i.text == "寫作比賽":
        continue
    elif i.text == " 歷屆比賽":
        continue
    elif i.text == "":
        continue
    elif i.text == "找比賽":
        break
    else:
        url_list.append(i.get_attribute("href"))
        title.append(i.text)


index = []
cTitle = []
for tit in title:
    if tit == '':
        continue
    else:
        cTitle.append(tit)


        
print(cTitle)

print(url_list)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

resource_path = "./projects"

if not os.path.exists(resource_path): 
    os.mkdir(resource_path)



for url in url_list:
    res = requests.get(url,headers = headers)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    js = soup.find('script')
    article = json.loads(js.text)
    if not os.path.isfile("./projects/index.json"): # initailize the json file
        with open("./projects/index.json", "w") as InitialFile:
            InitialFile.write("[]")

        
    with open("./projects/index.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
        jsonDict = json.load(JsonFile) 


    jsonDict.append(article) #add all every dic in to this list
        
    with open("./projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
        json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )