import requests
from bs4 import BeautifulSoup
import os
import json

o_url = "http://www.twctdf.com/news.php?wshop=twctdf&lang=zh-tw&Opt=search&searchkey=%E5%AD%B8%E7%94%9F%E8%B3%BD%E4%BA%8B"

titles = []
urls = []


resource_path = "./projects"

if not os.path.exists(resource_path):
    os.mkdir(resource_path)


header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

res = requests.get(o_url,header)
soup = BeautifulSoup(res.text,"html.parser")

entrys = soup.find_all("td",valign = "top")



for entry in entrys:
    if entry.text[0:4] != "2022":
        length = len(entry.text)
        if entry.text[length-2:length] != "公告":
            titles.append(entry.text.replace("\n","").replace("\xa0",""))
            print(entry.text)
            urls.append("http://www.twctdf.com/"+entry.a['href'])

for url in urls:
    
    res_next = requests.get(url,header)
    soup_next = BeautifulSoup(res_next.text,"html.parser")

    contents = soup_next.find("div",class_ = "post_content padding-3")
    content_list = []

    for content in contents.find_all('p'):
        content_list.append(content.text.replace(" ", "").replace("\r", "").replace("\xa0", ""))
    
    content_str = ' '.join(content_list)

    article ={
         "source_web_name":"中華民國競技飛鏢總會",
        "source_url":o_url,
        "url" : url,
        "title" : titles[urls.index(url)],
        "content" : content_str,
        "date" : None,
        "image":None,
        "id" : 0,
    }

    if not os.path.isfile("./projects/index.json"): # initailize the json file
        with open("./projects/index.json", "w") as InitialFile:
            InitialFile.write("[]")

        
    with open("./projects/index.json", "r", encoding="utf-8") as JsonFile: #transfer the article dic to json 
        jsonDict = json.load(JsonFile) 


    jsonDict.append(article) #add all every dic in to this list
        
    with open("./projects/index.json", "w",  encoding="utf-8") as writeFile: #write this to the json file
        json.dump( jsonDict , writeFile , ensure_ascii=False ,indent = 1 )