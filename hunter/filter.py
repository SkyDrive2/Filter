import json
import re
import copy
import datetime
import os

load = open("./projects/index.json", 'r' , encoding="utf-8" )
js = json.load(load)
load.close()
length = len(js)
title = []
content = []
sources = []
img = []
holder = []
con = []
start = []
end = []
Astart = []
AEnd = []


for i in range(0,length):
    title.append(js[i][0]["name"])
    content.append(js[i][0]["description"])
    sources.append(js[i][0]["url"])
    img.append(js[i][0]["image"])
    holder.append(js[i][0]["organizer"]["name"])
    contactPoint = {}
    contactPoint.update(js[i][0]["organizer"]["contactPoint"])
    EmandPh = []
    EmandPh.append("電子信箱："+contactPoint["email"])
    EmandPh.append("電話："+contactPoint["telephone"])
    con.append(EmandPh)
    start.append(js[i][0]["startDate"])
    end.append(js[i][0]["endDate"])
    As = {"活動日期":js[i][0]["subEvent"][0][0]["startDate"][:10]}
    Astart.append(As)
    AEnd.append(js[i][0]["subEvent"][0][0]["endDate"])




# for i in range(length):
#     print(js[i][1])
#     print()

for i in range(0,312):
    article ={
        "Title":title[i],
        "source":[sources[i]],
        "Content":content[i],
        "Connection":con[i],
        "Holder":[holder[i]],
        "Objective": None,
        "Image":img[i],
        "Subtitle":None,
        "Tags":None,
        "Branches":{
            "BranchName":"General",
            "DateStart":start[i][:10],
            "DateEnd":[end[i][:10]],
            "ApplyStart":Astart[i],
            "ApplyEnd":[AEnd[i][:10]],
            "ApplyFee":None,
            "Location":None
        }

    }

    if not os.path.isfile("./hunter/projects/filter.json"): # initailize the json file
        with open("./hunter/projects/filter.json", "w") as InitialFile:
            InitialFile.write("[]")

        
    with open("./hunter/projects/filter.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
        jsonDict = json.load(JsonFile) 


    jsonDict.append(article) #add all every dic in to this list
        
    with open("./hunter/projects/filter.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
        json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )
