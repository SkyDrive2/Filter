from bs4 import BeautifulSoup
import requests

url = "https://www.chgsh.chc.edu.tw/tag/game/"

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

res = requests.get(url , headers = headers)
soup = BeautifulSoup(res.text , "html.parser")

content_title = soup.find_all("h2",class_ = "blog-entry-title entry-title")

for title in content_title:
    print(title.a['href'])