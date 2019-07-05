from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'window-shopping'}
	
@view_config(route_name='fetch-products', renderer='jsonp')
def fetch_products(request):
	return {'project': 'window-shopping'}
