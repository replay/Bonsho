from wsgiref.simple_server import make_server
from pyramid import config


class ApiServer:

    def __init__(self):
        self.config = config.Configurator()
        self.config.scan('api.handlers')
        self.config.add_route('address_subscription', '/v1/add_address')
        self.app = self.config.make_wsgi_app()
        self.server = make_server('0.0.0.0', 8888, self.app)

    def run(self):
        self.server.serve_forever()
