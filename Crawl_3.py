# -*- coding: UTF-8 -*-
import io
import logging
import time
import requests
import json
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

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

logging.info('Set a dictionary to store info')
seller_sales = {}

##Open file sales_amount and set as write mode then put into 'Sellers_Sales_volume'
logging.info('Open file sales_amount and set as write mode then put into : Sellers_Sales_volume')
Sellers_Sales_volume = io.open("sales_amount.txt","w",encoding='utf-8')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}    
logging.info('Download the webdriver first, and enter the store path')
driver = webdriver.Chrome(executable_path=r"C:\Users\sarah.chao\Documents\Python\chromedriver_win32\chromedriver.exe")

#time.sleep(1)
logging.info('Let user enter the product keyword')
print("Please fill the name you want to search")
logging.info('Get the keyword')
item = input()

logging.info('Create two lists : shop_id and sale_vol to store follow-up processing data')
shop_id=[]
sale_vol=[]
logging.info('Make the window Full screen')
driver.maximize_window()

##Crawl 300 items, a page has 50 items so have to turn 6 pages'
logging.info('Crawl 300 items, a page has 50 items so have to turn 6 pages')
for page in range(6): 

    logging.info('Set the url, keyword, page')
    url = "https://shopee.tw/search?keyword="+str(item)+"&page="+str(page)
    
    logging.info('Driver get the url and pause action  (sleep) sleep to catch info')
    driver.get(url)
    time.sleep(3)
    logging.info('Let the window scroll down till the lowest section and pause action (sleep) to catch info')
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

    logging.info('Load the soup')
    soup = BeautifulSoup(driver.page_source,'lxml')

    logging.info('In order to crawl the info of html, make soup to find the class_ and capture sales and items')
    sales = soup.find_all("div", class_= "go5yPW")
    items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")

    logging.info('Capture the str within href and get the shop_id in Second to last')
    for shop in items:
        shops = shop.find("a")["href"]
        shop_id.append(shops.split(".")[-2])

    logging.info('Capture the str within sales and only get the sale_vol number, so store the second index. Besides, some items have not sales volume, need to give it 0')
    for sale in sales:
        if sale.text:
            sale_vol.append(sale.text.split(" ")[1])
        else:
            sale_vol.append('0')

    logging.info('Turn page')
    page += 1

logging.info('Once the capture is over, the browser closes')
driver.close()

logging.info('Calculate sale_vol, if appear "," then remove, and if appear "萬" then convert to float and *10000. Last, all sale_vol convert to int.')
for num in range(len(sale_vol)):
    ##remove the ','
    if "," in sale_vol[num]:
        sale_vol[num] = sale_vol[num].replace(",", "")

    ## convert the '萬'
    if "萬" in sale_vol[num]:
        number = float(sale_vol[num].replace("萬", "")) * 10000
        sale_vol[num] = number

    ## convert to int
    sale_vol[num] = int(sale_vol[num])

logging.info('Create a dictionary: seller_dict')
seller_dict = {}
logging.info('Put shop_id,sale_vol into seller_dict')
for key,value in zip(shop_id,sale_vol):
   seller_dict[key] = seller_dict.get(key,0)+value

logging.info('Create a dictionary: sorted_seller, ')
sorted_seller = {}
sorted_seller_2 = sorted(seller_dict, key=seller_dict.get,reverse=True)

logging.info('Get first 50 number , if less than 50 then get current quantity')
for seq in sorted_seller_2:
   if len(sorted_seller) < 50:
      sorted_seller[seq] = seller_dict[seq]
   else:
      break

logging.info('Create a list: store_file to temporary storage and set queue = 1')
store_file = []
queue = 1

logging.info('Finally, modify the foramt.')
for target in sorted_seller:
   print("The number", queue ,"shop is", target ,"with sales amount" ,sorted_seller[target])
   store_file = ("The number", queue ,"shop is", target ,"with sales amount", sorted_seller[target])
   Sellers_Sales_volume.write(str(store_file)+'\n') 
   queue += 1
