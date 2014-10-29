import json
from pyramid.view import view_config
from pyramid import response
from clients import manager


class AddressSubscriber:

    def __init__(self, request):
        self.request = request

    @view_config(route_name='address_subscriber', request_method='POST')
    def address_subscription(self):
        client_manager = manager.ClientManager.get_instance()
        data = json.loads(self.request.body.decode())
        client_manager.subscribe_address(data['address'])
        return response.Response('OK')
