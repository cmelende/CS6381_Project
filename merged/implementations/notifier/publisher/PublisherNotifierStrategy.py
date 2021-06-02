import json

import zmq

from merged.implementations.notifier.publisher.NotifierPublisher import NotifierPublisher
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.PublisherInfo import PublisherInfo
from merged.middleware.strategy.PublisherStrategy import PublisherStrategy


class PublisherNotifierStrategy(PublisherStrategy):

    def __init__(self, broker_info: BrokerInfo, publisher_info: PublisherInfo):
        self.__publisher_info = publisher_info
        self.__broker_info = broker_info
        self.__notifier_publishers: list[NotifierPublisher] = []
        self.__ctx = zmq.Context().instance()

    def register(self, topics: list[str]) -> None:
        publisher_port = self.__consume_port()
        self.__create_publisher(topics, publisher_port)
        self.__notify_broker_of_publisher(topics, publisher_port)

    def publish(self, topic: str, value: str) -> None:
        publisher: NotifierPublisher
        for publisher in self.__notifier_publishers:
            publisher.publish(topic, value)

    def close(self):
        publisher: NotifierPublisher
        for publisher in self.__notifier_publishers:
            publisher.close()
        self.__ctx.term()

    def __create_publisher(self, topics: list[str], publisher_port: str) -> None:
        publisher = NotifierPublisher(self.__publisher_info.PublisherAddress, publisher_port, topics)
        self.__notifier_publishers.append(publisher)

    def __notify_broker_of_publisher(self, topics: list[str], publisher_port: str) -> None:
        request_socket = self.__ctx.socket(zmq.REQ)

        request_socket.connect(f"tcp://{self.__broker_info.BrokerAddress}:{self.__broker_info.BrokerPort}")
        reg_body = {
            "ip": self.__publisher_info.PublisherAddress,
            "port": publisher_port,
            "topics": topics
        }
        request_socket.send_string(f'register${json.dumps(reg_body)}')
        resp = str(request_socket.recv(), encoding='utf-8')

    def __consume_port(self):
        if len(self.__publisher_info.PublisherPortPool) == 0:
            raise Exception("Out of ports")
        return self.__publisher_info.PublisherPortPool.pop(0)
