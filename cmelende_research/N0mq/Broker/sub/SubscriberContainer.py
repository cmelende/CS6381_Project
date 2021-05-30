import zmq

from cmelende_research.N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase
from cmelende_research.N0mq.Broker.sub.Subscriber import Subscriber


class SubscriberContainer:

    def __init__(self, host_address: str, port: str):
        self._context = zmq.Context().instance()
        self._port = port
        self._host_address = host_address
        self._subscribers: list[Subscriber] = list[Subscriber]()

    def register_sub(self, topic: str) -> None:
        subscriber = Subscriber(topic)
        subscriber.connect(self._host_address, self._port)
        self._subscribers.append(subscriber)
        pass

    def notify(self, topic: str, message_handler: MessageHandlerBase) -> None:
        for subscriber in self._subscribers:
            if subscriber.Topic == topic:
                subscriber.set_handler(message_handler)

    def listen(self) -> None:
        for subscriber in self._subscribers:
            subscriber.start()

    def close(self) -> None:
        for sub in self._subscribers:
            sub.close()
        self._context.term()
