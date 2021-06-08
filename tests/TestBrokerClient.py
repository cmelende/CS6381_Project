import unittest
from unittest.mock import Mock

from zmqmw.middleware.adapter.BrokerClient import BrokerClient


class TestBrokerClient(unittest.TestCase):
    def test_broker_strategy_run_called_when_client_run_called(self):
        strategy_mock = Mock()
        client = BrokerClient(strategy_mock)
        client.run()
        run_call_count = strategy_mock.run.call_count

        self.assertEqual(run_call_count, 1)

    def test_broker_strategy_close_called_when_client_close_called(self):
        strategy_mock = Mock()
        client = BrokerClient(strategy_mock)
        client.close()
        close_call_count = strategy_mock.close.call_count

        self.assertEqual(close_call_count, 1)


if __name__ == '__main__':
    unittest.main()
