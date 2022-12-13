import requests
from bs4 import BeautifulSoup
import os
import json
import time
from requests.adapters import HTTPAdapter


header  = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
hrefs = []
titles = []

for page in range(1,29):
    s =requests.session()
    s.mount("https://", HTTPAdapter(max_retries=3))
    o_url = "https://esshb.essh.kl.edu.tw/%e5%a4%9a%e5%85%83%e5%ad%b8%e7%bf%92%e8%b3%87%e8%a8%8a%e7%ab%99/?lcp_page0={}#lcp_instance_0".format(page)

    
    res = s.request("GET",o_url,header,timeout=3)
    soup = BeautifulSoup(res.text,"html.parser")

    urls = soup.find("ul" , class_ = "lcp_catlist")

    for url in urls.find_all("li"):

        hrefs.append(url.a['href'])

        titles.append(url.a.text)




resource_path = "./projects"

if not os.path.exists(resource_path):
    os.mkdir(resource_path)



for href in hrefs :

    s = requests.session()
    s.mount("https://", HTTPAdapter(max_retries=5))
    res_in = s.request("GET", href,header,timeout=4)
    
    soup_in = BeautifulSoup(res_in.text,"html.parser")

    contents = soup_in.find("div",class_ = "entry-content").text.replace(" ", "").replace("\r", "").replace("\xa0", "")

    img_list = []
    
    try:
        img = soup_in.find("img",decoding = "async")
        img_urls = img['srcset'].split(", ")
        
        for img_url in img_urls:
            if img_url !="https://secure.gravatar.com/avatar/924de1f0c4efd8d506e8508826a3cf45?s=98&d=mm&r=g":
                img_list.append(img_url.split(" ")[0])
    except TypeError as e:
        continue
    
   
    if img_list != [] or img_list == ["https://secure.gravatar.com/avatar/924de1f0c4efd8d506e8508826a3cf45?s=98&d=mm&r=g"]:
        article = {
            "source_web_name":"私立二信高級中學",
            "source_url":"https://esshb.essh.kl.edu.tw/",
            "url" : href,
            "title" : titles[hrefs.index(href)],
            "content" : contents,
            "date" : None,
            "image":img_list,
            "id" : 0,
        }
    else:
        article = {
            "source_web_name":"私立二信高級中學",
            "source_url":"https://esshb.essh.kl.edu.tw/",
            "url" : href,
            "title" : titles[hrefs.index(href)],
            "content" : contents,
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







