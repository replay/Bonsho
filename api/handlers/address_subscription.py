from pyramid.view import view_config
from pyramid import response


@view_config(route_name='address_subscription')
def address_subscription(request):
        return response.Response('Hello!')
