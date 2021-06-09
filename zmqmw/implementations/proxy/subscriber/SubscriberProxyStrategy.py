from zmqmw.base_classes.Logger import Logger
from zmqmw.implementations.proxy.subscriber.ProxySubscriber import ProxySubscriber
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.handler.MessageHandler import MessageHandler
from zmqmw.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberProxyStrategy(SubscriberStrategy):
    def __init__(self, broker_info: BrokerInfo, logger: Logger=Logger()):
        super().__init__(logger)
        self.__broker_xpub_port = broker_info.BrokerPubPort
        self.__broker_info = broker_info
        self.__subscribers: list[ProxySubscriber] = list[ProxySubscriber]()
        self.__keepRunning = True

    def unsubscribe(self, topic: str) -> None:
        sub: ProxySubscriber
        for sub in self.__subscribers:
            if topic == sub.Topic:
                sub.close()
                self.__subscribers.remove(sub)

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        subscriber = ProxySubscriber(topic, handlers)
        subscriber.connect(self.__broker_info.BrokerAddress, self.__broker_xpub_port)
        self._log_subscription(self.__broker_info.BrokerAddress, self.__broker_xpub_port, topic, handlers)
        self.__subscribers.append(subscriber)

    def listen(self, expected_count=None) -> None:
        count = expected_count if isinstance(expected_count, int) else -1

        while self.__keepRunning:
            sub: ProxySubscriber
            for sub in self.__subscribers:
                # self._log_listen(sub.Topic)
                sub.receive()
                count -= 1
                if count == 0:
                    self.__keepRunning = False

    def close(self) -> None:
        self.__keepRunning = False
        for sub in self.__subscribers:
            sub.close()
