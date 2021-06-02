import zmq

from merged.implementations.proxy.subscriber.ProxySubscriber import ProxySubscriber
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.handler.MessageHandler import MessageHandler
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberProxyStrategy(SubscriberStrategy):

    def __init__(self, broker_info: BrokerInfo):
        self.__broker_info = broker_info
        self.context = zmq.Context().instance()
        self.__subscribers: list[ProxySubscriber] = list[ProxySubscriber]()
        self.__keepRunning = True

    def unsubscribe(self, topic: str) -> None:
        sub: ProxySubscriber
        for sub in self.__subscribers:
            sub.close()
            self.__subscribers.remove(sub)
        pass

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        subscriber = ProxySubscriber(topic)
        subscriber.connect(self.__broker_info.BrokerAddress, self.__broker_info.BrokerPort)
        self.__subscribers.append(subscriber)

    def listen(self) -> None:
        while self.__keepRunning:
            sub: ProxySubscriber
            for sub in self.__subscribers:
                sub.receive()

    def close(self) -> None:
        self.__keepRunning = False
        for sub in self.__subscribers:
            sub.close()
