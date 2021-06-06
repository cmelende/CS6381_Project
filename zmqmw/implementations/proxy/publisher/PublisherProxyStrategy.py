import zmq

from zmqmw.base_classes.Logger import Logger
from zmqmw.implementations.proxy.publisher.ProxyPublisher import ProxyPublisher
from zmqmw.implementations.proxy.publisher.TopicsPublisherPair import TopicsPublisherPair
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.strategy.PublisherStrategy import PublisherStrategy


class PublisherProxyStrategy(PublisherStrategy):
    def __init__(self, broker_info: BrokerInfo, logger: Logger = Logger()):
        """
        Creates a new PublisherProxyStrategy object.
        :param broker_info: Required BrokerInfo object describing the broker.
        :param logger: An optional logger object implementing `zmqmw.base_classes.Logger`
        """
        super().__init__(logger)
        self.__broker_info = broker_info
        self.__topics_publisher_pairs: list[TopicsPublisherPair] = list[TopicsPublisherPair]()

    def register(self, topics: list[str]) -> None:
        publisher = ProxyPublisher()
        publisher.connect(self.__broker_info.BrokerAddress, self.__broker_info.BrokerSubPort)
        self._log_registration(self.__broker_info.BrokerAddress, self.__broker_info.BrokerSubPort, topics, publisher)

        topics_pub_pair = TopicsPublisherPair(topics, publisher)
        self.__topics_publisher_pairs.append(topics_pub_pair)

    def publish(self, topic: str, value: str) -> None:
        for pair in self.__topics_publisher_pairs:
            for pub_topic in pair.Topics:
                if pub_topic == topic:
                    pair.Publisher.publish(topic, value)
                    self._log_publish(topic, value)

    def close(self):
        for pub in self.__topics_publisher_pairs:
            pub.Publisher.close()
        zmq.Context().instance().term()
