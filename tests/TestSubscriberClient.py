import unittest
from unittest.mock import Mock

from zmqmw.middleware.adapter.SubscriberClient import SubscriberClient


class TestSubscriberClient(unittest.TestCase):
    def test_strategy_subscribe_called_when_client_subscribe_called(self):
        strategy_mock = Mock()
        client = SubscriberClient(strategy_mock)
        client.subscribe("", [])
        subscribe_call_count = strategy_mock.subscribe.call_count

        self.assertEqual(subscribe_call_count, 1)

    def test_strategy_unsubscribe_called_when_client_unsubscribe_called(self):
        strategy_mock = Mock()
        client = SubscriberClient(strategy_mock)
        client.unsubscribe("")
        unsubscribe_call_count = strategy_mock.unsubscribe.call_count

        self.assertEqual(unsubscribe_call_count, 1)


if __name__ == '__main__':
    unittest.main()
