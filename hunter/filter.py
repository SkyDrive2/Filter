import json
import re
import copy
import datetime
import os
import re
key = ["高中生", "高職生", "所有參賽者皆須持有中華民國國民身份證或本國居留證", "大專院校", "進修部", "碩、博士", "在職專班", "在臺就學之外籍學生", "高中職學生", "高中職生",
       "居住臺、澎、金、馬之中華民國國民", "五專", "高中職學校", "國小", "國中", "國民小學學生", "高中職師生", "中華民國各縣(市)公、私立學校之學生", "公、私立國民小學就讀中之學生"]


def ObjectiveFilter(content):
    objectiveList = []
    for i in key:
        if len(re.findall(i, content)) != 0:
            objectiveList.append(i)
    if len(objectiveList) == 0:
        return None
    else:
        return objectiveList

load = open("./projects/index1.json", 'r' , encoding="utf-8" )
js = json.load(load)
load.close()

load2  = open("./projects/filter_after.json" , 'r' , encoding="utf-8")
js2 = json.load(load2)
load2.close()

length = len(js)
length2 = len(js2)

print(length)
print(length2)
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
objective = []
tag = []








for i in range(0,length):
    title.append(js[i][0]["name"])
    content.append(js2[i]["Content"])
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
    tag.append(js2[i]["Tags"])


for cont in content:
    objective.append(ObjectiveFilter(cont))



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
        "Objective": objective[i],
        "Image":img[i],
        "Subtitle":None,
        "Tags":tag[i],
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

    if not os.path.isfile("./projects/filter(1).json"): # initailize the json file
        with open("./projects/filter(1).json", "w") as InitialFile:
            InitialFile.write("[]")

        
    with open("./projects/filter(1).json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
        jsonDict = json.load(JsonFile) 


    jsonDict.append(article) #add all every dic in to this list
        
    with open("./projects/filter(1).json", "w",  encoding="utf-8") as writeFile: #write this to the json file
        json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )
