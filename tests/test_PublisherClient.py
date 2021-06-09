import unittest
from unittest.mock import Mock

from zmqmw.middleware.adapter.PublisherClient import PublisherClient


class TestPublisherClient(unittest.TestCase):
    def test_strategy_register_called_when_client_register_called(self):
        strategy_mock = Mock()
        client = PublisherClient(strategy_mock)
        client.register([""])
        register_call_count = strategy_mock.register.call_count

        self.assertEqual(register_call_count, 1)

    def test_strategy_publish_called_when_client_publish_called(self):
        strategy_mock = Mock()
        client = PublisherClient(strategy_mock)
        client.publish("", "")
        publish_call_count = strategy_mock.publish.call_count

        self.assertEqual(publish_call_count, 1)

    def test_strategy_close_called_when_client_close_called(self):
        strategy_mock = Mock()
        client = PublisherClient(strategy_mock)
        client.close()
        close_call_count = strategy_mock.close.call_count

        self.assertEqual(close_call_count, 1)

