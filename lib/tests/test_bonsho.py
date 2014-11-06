import unittest
from unittest import mock
from lib import bonsho


class BonshoTest(unittest.TestCase):

    @mock.patch('lib.deduplicator.Deduplicator', autospec=True)
    @mock.patch('clients.manager.ClientManager', autospec=True)
    @mock.patch('api.server.ApiServer', autospec=True)
    def setUp(self, mock_api_server, mock_client_manager, mock_deduplicator):
        self.mock_api_server = mock_api_server
        self.mock_client_manager = mock_client_manager
        self.mock_deduplicator = mock_deduplicator
        self.bonsho = bonsho.Bonsho()

    @mock.patch('lib.deduplicator.Deduplicator')
    def test_run_shutdown(self, *args):
        self.bonsho.run()
        self.bonsho.deduper.run.assert_called_once_with()
        self.bonsho.client_manager.run_all.assert_called_once_with()
        self.bonsho.client_manager.subscribe.assert_called_once_with()
        self.bonsho.api.run.assert_called_once_with()
        self.bonsho.shutdown()
        self.bonsho.client_manager.shutdown.assert_called_once_with()
        self.bonsho.deduper.shutdown.assert_called_once_with()
