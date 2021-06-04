import json

import zmq

from merged.examples.misc.logger.Logger import Logger
from merged.examples.misc.value_objects.TopicHandlers import TopicHandler
from merged.implementations.AvailablePublishers import AvailablePublishers
from merged.implementations.notifier.subscriber.NotifierSubscriber import NotifierSubscriber
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.handler.MessageHandler import MessageHandler
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberNotifierStrategy(SubscriberStrategy):
    def __init__(self, broker_info: BrokerInfo, logger: Logger, topic_handlers: list[TopicHandler]):
        super().__init__(logger)
        self.__topic_handlers = topic_handlers
        self.__broker_info = broker_info
        self.__keepRunning = True
        self.__subscribers: list[NotifierSubscriber] = list[NotifierSubscriber]()

    def unsubscribe(self, topic: str) -> None:
        subscriber: NotifierSubscriber
        for subscriber in self.__subscribers:
            subscriber.close()
            self.__subscribers.remove(subscriber)

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        available_publishers = self.get_available_publishers_by_topic(self.__broker_info, topic)
        for available_publisher in available_publishers:
            if topic in available_publisher.Topics:
                subscriber = NotifierSubscriber(topic, handlers)
                subscriber.connect(available_publisher.Host, available_publisher.Port)
                self._log_subscription(available_publisher.Host, available_publisher.Port, topic, handlers)
                self.__subscribers.append(subscriber)

    def listen(self) -> None:
        while self.__keepRunning:
            sub: NotifierSubscriber
            for sub in self.__subscribers:
                # self._log_listen(sub.Topic)
                sub.receive()

    def close(self) -> None:
        self.__keepRunning = False
        for sub in self.__subscribers:
            sub.close()

    @staticmethod
    def get_available_publishers_by_topic(broker_info: BrokerInfo, topic: str) -> list[AvailablePublishers]:
        ctx = zmq.Context().instance()
        s = ctx.socket(zmq.REQ)
        s.connect(f"tcp://{broker_info.BrokerAddress}:{broker_info.BrokerPort}")
        s.send_string(f"request${topic}")
        topics = json.loads((s.recv()))

        items = topics.items()

        available_publishers: list[AvailablePublishers] = list[AvailablePublishers]()
        for k, v in items:
            available_publishers.append(AvailablePublishers(v['ip'], v['port'], v['topics']))

        return available_publishers