from requests import Request, post
from pyquery import PyQuery as pq
import copy
import json
import multiprocessing
from time import sleep
import sys
from .Scrapper import Scrapper
from .JSONSerializeable import JSONSerializeable

class Product(JSONSerializeable):
	def __init__(self, name=None, price=None, picture=None, link=None):
		self.name = name
		self.price = price
		self.picture = picture
		self.link = link
	
	def setName(self, name):
		self.name = name
	
	def setPrice(self, price):
		self.price = price
	
	def setPicture(self, picture):
		self.picture = picture
	

class Shopaholic(object):
	def __init__(self):
		self.url_bl = None
		self.url_toped = None
		self.store_id_bl = None
		pass
	
	def setStoreIdBL(self, store_id):
		self.store_id_bl = store_id
	
	def setUrlBL(self, url_bl):
		self.url_bl = url_bl
	
	def setUrlToped(self, url):
		self.url_toped = url
	
	def daemonize(self):
		manager = multiprocessing.Manager()
		return_dict = manager.dict()
		
		jobs = []
		p_bl = multiprocessing.Process(target=self.fetchProductBL, args=(0,return_dict))
		p_bl.daemon = True
		jobs.append(p_bl)
		p_bl.start()
		p_tp = multiprocessing.Process(target=self.fetchProductToped, args=(1,return_dict))
		p_tp.daemon = True
		jobs.append(p_tp)
		p_tp.start()
		
		for proc in jobs:
			proc.join()
		
		return return_dict.values()
		
	
	def fetchProductBL(self, procnum, return_dict):
		number_per_page = 80
		page_number = 1
		# url_toko = 'https://www.bukalapak.com/u/toko_berkat_melimpah'
		# store_id = '71665369'

		url_target = self.url_bl

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

		url_product = 'https://api.bukalapak.com/stores/' + self.store_id_bl + '/products?offset=' + str(offset) +' &limit=16&sort=bestselling&access_token=' + token

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
			product = Product(**matrix)
			parsed_product.append(copy.copy(product))

		print(parsed_product)
		return_dict[procnum] = parsed_product
	
	
	def fetchProductToped(self, procnum, return_dict):
		number_per_page = 80
		page_number = 1
		url_target = self.url_toped

		if (page_number > 1):
			url_target += '/page/' + str(page_number)

		if (number_per_page == 40 or number_per_page == 20):
			url_target += '?perpage=' + str(number_per_page)
			
		scrapper = Scrapper()
		strip_ = scrapper.requestData(url=url_target)
		#strip_ = response.text.replace('\n', '').replace('\\u002F', '/').replace('\\"','"')
		products = pq(strip_)('a.css-aobwgn')

		parsed_product = []
		number_per_page = int(pq(strip_)('.css-merchant-3YUK2I23')('.css-merchant-1WMdr3A_').text())

		for each_product in products:
			matrix = {}
			matrix['name'] = pq(each_product)('div .css-merchant-2xnEppWk').text()
			matrix['picture'] = pq(each_product)('div img').attr('src')
			matrix['link'] = pq(each_product)('a').attr('href')
			matrix['price'] = pq(each_product)('div .css-merchant-mqaiMy5d').text()
			product = Product(**matrix)
			parsed_product.append(copy.copy(product))

		print(parsed_product)
		print(number_per_page)
		
		return_dict[procnum] = parsed_product