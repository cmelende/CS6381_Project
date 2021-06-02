from merged.examples.misc.logger.Logger import Logger
from merged.implementations.notifier.subscriber.NotifierSubscriber import NotifierSubscriber
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.handler.MessageHandler import MessageHandler
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberNotifierStrategy(SubscriberStrategy):
    def __init__(self, broker_info: BrokerInfo, logger: Logger):
        super().__init__(logger)
        self.__broker_info = broker_info
        self.__keepRunning = True
        self.__subscribers: list[NotifierSubscriber] = list[NotifierSubscriber]()

    def unsubscribe(self, topic: str) -> None:
        subscriber: NotifierSubscriber
        for subscriber in self.__subscribers:
            subscriber.close()
            self.__subscribers.remove(subscriber)

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        subscriber = NotifierSubscriber(topic, handlers)
        subscriber.connect(self.__broker_info.BrokerAddress, self.__broker_info.BrokerPort)
        self._log_subscription(self.__broker_info.BrokerAddress, self.__broker_info.BrokerPort, topic, handlers)
        self.__subscribers.append(subscriber)

    def listen(self) -> None:
        while self.__keepRunning:
            sub: NotifierSubscriber
            for sub in self.__subscribers:
                self._log_listen(sub.Topic)
                sub.receive()

    def close(self) -> None:
        self.__keepRunning = False
        for sub in self.__subscribers:
            sub.close()
