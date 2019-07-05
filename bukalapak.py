from requests import Request, post
from pyquery import PyQuery as pq
import copy
import json

number_per_page = 80
page_number = 1
url_toko = 'https://www.bukalapak.com/u/toko_berkat_melimpah'
store_id = '71665369'

url_target = url_toko

if (page_number > 1):
	url_target += '?page=' + str(page_number)

#if (number_per_page == 40 or number_per_page == 20):
#url_target += '?perpage=' + str(number_per_page)

url = 'http://localhost:2233/rest'
response = post(url, data = {'url': url_target, 'method' : 'GET', })
strip_ = response.text.replace('\n', '').replace('\\u002F', '/').replace('\\"','"')

url_req_token = 'https://www.bukalapak.com/auth_proxies/request_token'

url = 'http://localhost:2233/rest'
response = post(url, data = {'url': url_req_token, 'method' : 'POST', })
token = json.loads(response.text)['data']['access_token']

offset = 0

url_product = 'https://api.bukalapak.com/stores/' + store_id + '/products?offset=' + str(offset) +' &limit=16&sort=bestselling&access_token=' + token

url = 'http://localhost:2233/rest'
response = post(url, data = {'url': url_product, 'method' : 'GET', })
products = json.loads(response.text)['data']['data']

parsed_product = []

for each_product in products:
	matrix = {}
	matrix['name'] = each_product['name']
	matrix['picture'] = each_product['images']['large_urls'][0]
	matrix['link'] = each_product['url']
	matrix['price'] = each_product['price']
	parsed_product.append(copy.copy(matrix))

print(parsed_product)

