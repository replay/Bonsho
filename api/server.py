from wsgiref.simple_server import make_server
from pyramid import config as pyramid_config
from lib import config as project_config


class ApiServer:

    def __init__(self):
        self.config = pyramid_config.Configurator()
        self.config.scan('api.handlers')
        self.config.add_route('address_subscriber', '/v1/add_address')
        self.app = self.config.make_wsgi_app()
        config = project_config.Configuration()['API']
        self.server = make_server(
            config['Host'],
            int(config['Port']),
            self.app)

    def run(self):
        self.server.serve_forever()
