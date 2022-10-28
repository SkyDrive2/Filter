from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='./chromedriver.exe')

url = "https://www.chgsh.chc.edu.tw/tag/game/"

driver.get(url) # 更改網址以前往不同網頁


prev_ele = None
while True:
    eles = dirver.find_elements_by_class_name('blog-entry-title entry-title')
    try:
        eles = eles[eles.index(prev_ele):]
    except:
        pass
    for ele in eles:
        try:
            title = ele.find_element_by_class_name("69")
driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")



print()