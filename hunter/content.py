import json
import re
import copy
import datetime
import os

load = open("./projects/index.json", 'r' , encoding="utf-8" )
js = json.load(load)
load.close()
length = len(js)


for j in js:
    string = j["content"]

    if string == "\n\n":
        continue
    else:
        article ={
            "source_web_name":"獎金獵人",
            "source_url": "https://bhuntr.com/tw",
            "url" : j["url"],
            "title" : j["title"],
            "content" : string,
            "date":None,
            "image":j["image"],
            "Id": 0
        }
        if not os.path.isfile("./projects/index2.json"): # initailize the json file
            with open("./projects/index2.json", "w") as InitialFile:
                InitialFile.write("[]")

        
        with open("./projects/index2.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
            jsonDict = json.load(JsonFile) 


        jsonDict.append(article) #add all every dic in to this list

        with open("./projects/index2.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
            json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )