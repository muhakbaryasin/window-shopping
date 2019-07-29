from pyramid.view import view_config
from .Shopaholic import Shopaholic

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'window-shopping'}
	
@view_config(route_name='fetch-products', renderer='jsonp')
def fetch_products(request):
	shop = Shopaholic()
	shop.setUrlBL('https://www.bukalapak.com/u/toko_berkat_melimpah')
	shop.setStoreIdBL('71665369')
	shop.setUrlToped('https://www.tokopedia.com/tkberkatmelimpah')
	stores = []
	stores = shop.daemonize()
	
	the_list = []
	
	for each_store in stores:
		the_list += each_store
		
	#anu = {}
	#tes = shop.fetchProductBL(1, anu)
	#print(tes)
	return {'code': 'OK', 'data': {'products': the_list}, 'message' : ''}
	
@view_config(route_name='fetch-products-html', renderer='templates/products.jinja2')
def my_view(request):
	shop = Shopaholic()
	shop.setUrlBL('https://www.bukalapak.com/u/toko_berkat_melimpah')
	shop.setStoreIdBL('71665369')
	shop.setUrlToped('https://www.tokopedia.com/tkberkatmelimpah')
	stores = []
	stores = shop.daemonize()

	the_list = []

	for each_store in stores:
		the_list += each_store

	return {'products': the_list}
