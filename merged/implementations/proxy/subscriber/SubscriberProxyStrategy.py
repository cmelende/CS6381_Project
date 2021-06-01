import zmq

from merged.implementations.proxy.subscriber.Subscriber import Subscriber
from merged.middleware.handler.MessageHandler import MessageHandler
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberProxyStrategy(SubscriberStrategy):

    def __init__(self, host_address: str, port: str):
        self.context = zmq.Context().instance()
        self.__port = port
        self.__host_address = host_address
        self.__subscribers: list[Subscriber] = list[Subscriber]()
        self.__keepRunning = True

    def unsubscribe(self, topic: str) -> None:
        sub: Subscriber
        for sub in self.__subscribers:
            sub.close()
            self.__subscribers.remove(sub)
        pass

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        subscriber = Subscriber(topic)
        subscriber.connect(self.__host_address, self.__port)
        self.__subscribers.append(subscriber)

    def listen(self) -> None:
        while self.__keepRunning:
            sub: Subscriber
            for sub in self.__subscribers:
                sub.receive()

    def close(self) -> None:
        self.__keepRunning = False
        for sub in self.__subscribers:
            sub.close()
