import unittest
from unittest.mock import Mock
from time import sleep
from zmqmw.implementations.notifier.publisher.PublisherNotifierStrategy import PublisherNotifierStrategy
from zmqmw.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy
from zmqmw.implementations.proxy.publisher.PublisherProxyStrategy import PublisherProxyStrategy
from zmqmw.implementations.proxy.subscriber.SubscriberProxyStrategy import SubscriberProxyStrategy
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.PublisherInfo import PublisherInfo
from zmqmw.middleware.adapter.BrokerClient import BrokerClient
from zmqmw.middleware.adapter.PublisherClient import PublisherClient
from multiprocessing import Process, Value

from zmqmw.middleware.adapter.SubscriberClient import SubscriberClient
from zmqmw.middleware.handler.MessageHandler import MessageHandler


class TestHandler(MessageHandler):
    def __init__(self, v):
        self.value = v

    def handle_message(self, value: str) -> None:
        self.value.value += int(value.split(":")[1])


def start_proxy():
    broker = BrokerProxyStrategy(broker_address="127.0.0.1",
                                 broker_xpub_port=6000,
                                 broker_xsub_port=7000)
    proxy = BrokerClient(broker)
    proxy.run()


def start_subscriber(th):
    broker = BrokerInfo(broker_address="127.0.0.1", broker_pub_port=6000)
    strategy = SubscriberProxyStrategy(broker_info=broker)
    subscriber = SubscriberClient(subscriber_strategy=strategy)
    subscriber.subscribe(topic='test', handlers=[th])
    try:
        subscriber.listen()
    except Exception:
        subscriber.close()


def start_publisher():
    broker = BrokerInfo(broker_address="127.0.0.1", broker_sub_port=7000)
    strategy = PublisherProxyStrategy(broker_info=broker)
    publisher = PublisherClient(strategy=strategy)
    publisher.register(topics=['test'])

    for i in range(26):
        publisher.publish(topic='test', val=1)
        sleep(0.1)


class TestRun(unittest.TestCase):
    def test_proxy_run(self):
        v: Value = Value('d', 0)
        th = TestHandler(v)

        proxy = Process(target=start_proxy, args=())
        proxy.start()

        subscriber = Process(target=start_subscriber, args=[th])
        subscriber.start()

        publisher = Process(target=start_publisher, args=())
        publisher.start()

        sleep(3)
        proxy.terminate()
        subscriber.terminate()
        publisher.terminate()

        self.assertEqual(25.0, v.value)
