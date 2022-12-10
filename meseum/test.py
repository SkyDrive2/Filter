import requests
from bs4 import BeautifulSoup

o_url = "https://www.ntmofa.gov.tw/activitysoonlist_1052_2.html"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}


res = requests.get(o_url,headers)
soup = BeautifulSoup(res.text,"html.parser")

urls = soup.find_all("span",class_ = "date")
date = []
for url in urls:
    date.append(url.text.replace(" ", "").replace("\r", "").replace("\xa0", "").replace("\n",""))
print(len(date))