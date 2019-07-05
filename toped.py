import pdb
from requests import Request, post
from pyquery import PyQuery as pq
import copy

number_per_page = 80
page_number = 1
url_toko = 'https://www.tokopedia.com/ascaryacomp'

url_target = url_toko

if (page_number > 1):
	url_target += '/page/' + str(page_number)

if (number_per_page == 40 or number_per_page == 20):
	url_target += '?perpage=' + str(number_per_page)

url = 'http://localhost:2233/rest'
response = post(url, data = {'url': url_target, 'method' : 'GET', })
strip_ = response.text.replace('\n', '').replace('\\u002F', '/').replace('\\"','"')
products = pq(strip_)('a.css-aobwgn')

parsed_product = []
number_per_page = int(pq(strip_)('.css-merchant-3YUK2I23')('.css-merchant-1WMdr3A_').text())

for each_product in products:
	matrix = {}
	matrix['name'] = pq(each_product)('div .css-merchant-2xnEppWk').text()
	matrix['picture'] = pq(each_product)('div img').attr('src')
	matrix['link'] = pq(each_product)('a').attr('href')
	matrix['price'] = pq(each_product)('div .css-merchant-mqaiMy5d').text()
	parsed_product.append(copy.copy(matrix))

print(parsed_product)
print(number_per_page)
