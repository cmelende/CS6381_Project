import zmq

from merged.implementations.proxy.publisher.Publisher import Publisher
from merged.implementations.proxy.publisher.TopicsPublisherPair import TopicsPublisherPair
from merged.middleware.strategy.PublisherStrategy import PublisherStrategy


class PublisherProxyStrategy(PublisherStrategy):
    def __init__(self, host: str, port: str):
        self.__host = host
        self.__port = port
        self.__topics_publisher_pairs: list[TopicsPublisherPair] = list[TopicsPublisherPair]()

    def register(self, topics: list[str]):
        publisher = Publisher()
        publisher.connect(self.__host, self.__port)
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
