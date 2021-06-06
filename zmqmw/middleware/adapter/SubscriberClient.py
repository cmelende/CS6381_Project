from zmqmw.middleware.handler.MessageHandler import MessageHandler
from zmqmw.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberClient:
    def __init__(self, subscriber_strategy: SubscriberStrategy):
        """
        The SubscriberClient we need to subscribe to a publisher.

        :param subscriber_strategy: A required strategy used by the Subscriber.
        """
        self._subscriber_strategy: SubscriberStrategy = subscriber_strategy

    def set_strategy(self, subscriber_strategy: SubscriberStrategy):
        self._subscriber_strategy = subscriber_strategy

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        """
        Subscribe to a topic and specify how to handle the events from said topic.

        :param topic: A topic in which we are interested
        :param handlers: A list of handlers (subclassed from `MessageHandler`)
        :return: None
        """
        self._subscriber_strategy.subscribe(topic, handlers)

    def unsubscribe(self, topic: str) -> None:
        self._subscriber_strategy.unsubscribe(topic)

    def listen(self, expected_count=None) -> None:
        self._subscriber_strategy.listen(expected_count=expected_count)

    def close(self):
        self._subscriber_strategy.close()
