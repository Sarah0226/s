#Crawl 
# -*- coding: UTF-8 -*-
##到蝦皮首頁搜尋iphone x，並抓前300個商品的銷售量以及shopid
import io
import logging
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

##Create a file and setting its format
log_format = "%(asctime)s %(levelname)s Line %(lineno)d: %(message)s"

##Create a new log file each time and file name added current time
logdatetime = time.strftime("%Y-%m-%d_%H-%M-%S")
logging.basicConfig(filename="Objective_3_"+ logdatetime + ".log", filemode="w", level=logging.DEBUG, format=log_format)

##Print the log on terminal, so use streamhandler, then setting its format
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler_format = logging.Formatter("%(asctime)s %(levelname)s: Line %(lineno)d: %(message)s")
handler.setFormatter(handler_format)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

url = "https://shopee.tw/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}    
driver = webdriver.Chrome(executable_path=r"C:\Users\sarah.chao\Documents\Python\chromedriver_win32\chromedriver.exe") #, chrome_options = options)
driver.maximize_window()
driver.get(url)
res = driver.page_source
soup = BeautifulSoup(res,'lxml')
q = driver.find_element_by_class_name('shopee-searchbar-input__input')
print("Please fill the name you want to search")
item = str(input())
q.send_keys(item)
q.send_keys(Keys.RETURN)

#logging.info('soup')
#soup = BeautifulSoup(driver.page_source,'lxml')
#logging.info('links')
#sale = soup.find_all("div", class_ = "go5yPW")
#print (sale)
#logging.info('ne')
#next_page = soup.find(class_ ="shopee-icon-button shopee-icon-button--right")

##Open file sales_amount and set as write mode then put into 'sale'
sale = io.open("sales_amount.txt","w",encoding='utf-8')
#index = 0
page = 0
data = []
while page < 7: ###抓300個商品，一頁50個要6頁
    soup = BeautifulSoup(driver.page_source,'lxml')
    for amount in soup.find_all(class_="go5yPW"):
        #sell = BeautifulSoup(driver.page_source,'lxml')
        data.append(selling_data = list(amount))
        print(data)
        sale.write(data + '\n')
    page = page +1

    

#driver.close()
