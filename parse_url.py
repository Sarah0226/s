import requests
from bs4 import BeautifulSoup
import urllib

url = 'https://shopee.tw/search'

my_params = {'keyword': 'iphone x'}

headers = {'Content-Type': 'application/json;charset=UTF-8'}

params = urllib.parse.urlencode(my_params, quote_via=urllib.parse.quote)

r = requests.get(url, params=params)

print(r.url)
print(r.text)
