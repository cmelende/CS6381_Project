import unittest
from unittest.mock import Mock

from zmqmw.implementations.notifier.publisher.PublisherNotifierStrategy import PublisherNotifierStrategy
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.PublisherInfo import PublisherInfo
from zmqmw.middleware.adapter.BrokerClient import BrokerClient
from zmqmw.middleware.adapter.PublisherClient import PublisherClient


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

    def test_strategy_instantiates_correct_object(self):
        broker = BrokerInfo(broker_address="127.0.0.1", broker_sub_port=6000)
        self.assertIsInstance(broker, BrokerInfo)

        pub_info = PublisherInfo(publisher_address="127.0.0.1", publisher_port=7000)
        self.assertIsInstance(pub_info, PublisherInfo)

        strategy = PublisherNotifierStrategy(broker_info=broker, publisher_info=pub_info)
        self.assertIsInstance(strategy, PublisherNotifierStrategy)

        publisher = PublisherClient(strategy=strategy)
        self.assertIsInstance(publisher, PublisherClient)
