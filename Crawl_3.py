# -*- coding: UTF-8 -*-
##到蝦皮首頁搜尋iphone x，並抓前300個商品的銷售量以及shopid
import io
import logging
import time
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

seller_sales = {}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}    
driver = webdriver.Chrome(executable_path=r"C:\Users\sarah.chao\Documents\Python\chromedriver_win32\chromedriver.exe")

time.sleep(1)

#q = driver.find_element_by_class_name('shopee-searchbar-input__input')
print("Please fill the name you want to search")
item = str(input())
#page = 0
shop_id=[]
sale_vol=[]


##抓300個商品，一頁50個要6頁
for page in range(6): 
    url = "https://shopee.tw/search?keyword="+item+"&page="+ str(page)
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 1000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 1500)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 2000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 2500)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 3000)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source,'lxml')

    sales = soup.find_all("div", class_= "go5yPW")
    items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")


    for shop in items:
        shops = shop.find("a")["href"]
        shop_id.append(shops.split(".")[-2])
        #print(shop_id)
 
    for sale in sales:
        if sale.text:
            sale_vol.append(sale.text.split(" ")[1])
        else:
            sale_vol.append(0)

        #sale_vol = sale_vol.replace(",","")
        sale_vol=int(sale_vol)
        #print(sale_vol)
    
    seller_sales = dict(zip(shop_id,sale_vol))
    # = int(sale_vol)
    print(shop_id)
    print (len(shop_id))
    print(sale_vol)
    print (len(sale_vol))
    print(seller_sales)
    page =+ 1


##Open file sales_amount and set as write mode then put into 'sale'
sale = io.open("sales_amount.txt","w",encoding='utf-8')


#driver.close()
