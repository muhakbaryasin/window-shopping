import http.cookiejar
import urllib.request
import urllib.parse
from urllib.parse import urlencode, unquote
import re
from .FileLogger import FileLogger

import gzip
import datetime
import time

class Scrapper(object):
	def __init__(self):
		"""
		kwarg
		**urllibArg = {url, data, headers={}, origin_req_host=None, unverifiable=False, method=None}
		urllib.request.Request()
		"""
		self.cookiejar = http.cookiejar.CookieJar()
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
		self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36')]
	
	def requestData(self, file_log_name = None, referer = None, x_requested_with = None, **urllibArg):
		try:
			# This is the Request
			req = urllib.request.Request(**urllibArg)
			print("Request -> " + urllibArg['url'])
			if referer is not None :
				req.add_header('Referer', referer)
			if x_requested_with is not None:
				req.add_header('X-Requested-With', x_requested_with)
			site = self.opener.open(req)
			
			response_data = None
			
			if site.info().get('Content-Encoding') == 'gzip':
				response_data = gzip.decompress( site.read() )
			else:
				response_data = site.read()

			if file_log_name is not None :
				fileLogger = FileLogger(file_log_name=file_log_name, data=response_data, mode="wb")
		except Exception as e:
			response_data = None
			reference = urllibArg['url']
			message = str(urllibArg)
			timestampString = datetime.datetime.fromtimestamp(time.time()).strftime('%b-%H')
			fileLogger = FileLogger(file_log_name=('request-data-' + timestampString + '.txt') ,reference=reference, data=message, exception=e, mode="a")
		return response_data

	def getSession(self):
		return self.opener

	def setSession(self, opener):
		self.opener = opener
