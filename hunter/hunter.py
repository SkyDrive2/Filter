import json
import re
import copy
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

load = open("./projects/filter.json", 'r' , encoding="utf-8" )
js = json.load(load)
load.close()
length = len(js)
all_url = []

for i in js:
    all_url.append(i['source'][0])

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path = './chromedriver.exe',options=chrome_options)


for url in all_url:
    driver.get(url)
    contents = driver.find_elements(By.TAG_NAME,"p")
    string = ""
    for content in contents:
        string+=content.text

    article ={
        "Contents" : content
    }
    if not os.path.isfile("./projects/content.json"): # initailize the json file
        with open("./projects/content.json", "w") as InitialFile:
            InitialFile.write("[]")

        
    with open("./projects/content.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
        jsonDict = json.load(JsonFile) 


    jsonDict.append(article) #add all every dic in to this list
        
    with open("./projects/content.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
        json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )