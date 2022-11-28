from bs4 import BeautifulSoup
import requests
import json

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

url = "https://bhuntr.com/tw/competitions/3airrdw8ame9ict69y"

res = requests.get(url,headers = headers)
res.encoding='utf-8'

soup = BeautifulSoup(res.text)
# string = "application/ld+json"
# contents = soup.find_all("script",type = string) 
print(soup.find("div"))



# i = contents[0]
# test = json.loads(i.text)
# open("tst.json", "w", encoding="utf-8").write(json.dumps(test, indent=4,ensure_ascii=False))  

