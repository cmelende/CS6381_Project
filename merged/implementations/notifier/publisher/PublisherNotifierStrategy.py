import json
import zmq

from merged.examples.misc.logger.Logger import Logger
from merged.implementations.notifier.publisher.NotifierPublisher import NotifierPublisher
from merged.implementations.notifier.publisher.TopicsNotifierPublisherPair import TopicsNotifierPublisherPair
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.PublisherInfo import PublisherInfo
from merged.middleware.strategy.PublisherStrategy import PublisherStrategy


class PublisherNotifierStrategy(PublisherStrategy):

    def __init__(self, broker_info: BrokerInfo, publisher_info: PublisherInfo, logger: Logger):
        super().__init__(logger)
        self.__publisher_info = publisher_info
        self.__broker_info = broker_info
        self.__topics_publisher_pairs: list[TopicsNotifierPublisherPair] = list[TopicsNotifierPublisherPair]()
        self.__ctx = zmq.Context().instance()

    def register(self, topics: list[str]) -> None:
        publisher_port = self.__consume_port()
        self.__create_publisher(topics, publisher_port)
        self.__notify_broker_of_publisher(topics, publisher_port)

    def publish(self, topic: str, value: str) -> None:
        for pair in self.__topics_publisher_pairs:
            for pub_topic in pair.Topics:
                if pub_topic == topic:
                    pair.Publisher.publish(topic, value)
                    self._log_publish(topic, value)

    def close(self):
        for pub in self.__topics_publisher_pairs:
            pub.Publisher.close()
        self.__ctx.term()

    def __create_publisher(self, topics: list[str], publisher_port: str) -> None:
        publisher = NotifierPublisher()
        publisher.connect(self.__publisher_info.PublisherAddress, publisher_port)
        self._log_registration(self.__publisher_info.PublisherAddress, publisher_port, topics, publisher)

        topics_pub_pair = TopicsNotifierPublisherPair(topics, publisher)
        self.__topics_publisher_pairs.append(topics_pub_pair)

    def __notify_broker_of_publisher(self, topics: list[str], publisher_port: str) -> None:
        request_socket = self.__ctx.socket(zmq.REQ)

        url = f'{self.__broker_info.BrokerAddress}:{self.__broker_info.BrokerPort}'
        request_socket.connect(f"tcp://{url}")
        self._log_socket_connection(url, "REQ")

        reg_body = {
            "ip": self.__publisher_info.PublisherAddress,
            "port": publisher_port,
            "topics": topics
        }
        payload = f'register${json.dumps(reg_body)}'
        request_socket.send_string(payload)
        self._log_send(url, payload)

        resp = str(request_socket.recv(), encoding='utf-8')
        self._log_recv(url, resp)

    def __consume_port(self):
        if len(self.__publisher_info.PublisherPortPool) == 0:
            raise Exception("Out of ports")
        return self.__publisher_info.PublisherPortPool.pop(0)
