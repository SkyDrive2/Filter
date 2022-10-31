from bs4 import BeautifulSoup
import requests

url = "https://www.chgsh.chc.edu.tw/tag/game/"



res = requests.get(url , headers = headers)
soup = BeautifulSoup(res.text , "html.parser")

print(soup)
content_title = soup.find_all("h2",class_ = "blog-entry-title entry-title")
url_list = []

for title in content_title:
    url_list.append(title.a['href'])

print(len(url_list))