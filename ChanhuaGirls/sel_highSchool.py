from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
driver = webdriver.Chrome(executable_path = './chromedriver.exe')

url = "https://www.chgsh.chc.edu.tw/tag/game/"
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

driver.get(url) # 更改網址以前往不同網頁

temp_height = 0

prev_ele = None
while True:
    driver.execute_script("window.scrollBy(0,1000)")

    check_height = driver.execute_script("return document.      documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")

    if check_height == temp_height:
        break
    temp_height = check_height
time.sleep(2)

soup = BeautifulSoup(driver.page_source,"html.parser")


first = soup.find("div",{"id":"content"})

element = first.find_all("h2",{"class":"blog-entry-title entry-title"})

url_list = []
url_title = []
for title in element:
    url_title.append(title.a['title'])
    url_list.append(title.a['href'])



for i in url_list:
    res = requests.get(i,headers = headers)
    small_soup = BeautifulSoup(res.text,"html.parser")
    
    contents = small_soup.find_all("div",class_ = "entry-content clr")

    con = []
    for content in contents:
        con.append(content.p.text)

    print(con)


