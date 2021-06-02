import random

import zmq

from merged.implementations.proxy.publisher.ProxyPublisher import ProxyPublisher
from merged.implementations.proxy.publisher.TopicsPublisherPair import TopicsPublisherPair
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.strategy.PublisherStrategy import PublisherStrategy


class PublisherProxyStrategy(PublisherStrategy):
    def __init__(self, broker_info: BrokerInfo):
        self.__broker_info = broker_info
        self.__topics_publisher_pairs: list[TopicsPublisherPair] = list[TopicsPublisherPair]()

    def register(self, topics: list[str]):
        publisher = ProxyPublisher()
        publisher.connect(self.__broker_info.BrokerAddress, self.__broker_info.BrokerPort)
        topics_pub_pair = TopicsPublisherPair(topics, publisher)
        self.__topics_publisher_pairs.append(topics_pub_pair)

    def publish(self, topic: str, value: str) -> None:
        for pair in self.__topics_publisher_pairs:
            for pub_topic in pair.Topics:
                if pub_topic == topic:
                    pair.Publisher.publish(topic, value)

    def close(self):
        for pub in self.__topics_publisher_pairs:
            pub.Publisher.close()
        zmq.Context().instance().term()

