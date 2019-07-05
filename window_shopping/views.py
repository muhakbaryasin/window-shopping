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
	tes = shop.daemonize()
	import pdb; pdb.set_trace()
	#anu = {}
	#tes = shop.fetchProductToped(1, anu)
	return {'project': 'window-shopping', 'products': tes}
