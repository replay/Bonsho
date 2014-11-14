import json
from lib import address_filter
from pyramid.view import view_config
from pyramid import response


class AddressSubscriber:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='address_subscription', request_method='POST')
    def address_subscription(self):
        af = address_filter.AddressFilter()
        data = json.loads(self.request.body.decode())
        if data['action'] == 'subscribe':
            af.add_address(data['address'])
        if data['action'] == 'unsubscribe':
            af.del_address(data['address'])
        return response.Response('OK')
