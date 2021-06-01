from merged.middleware.handler.MessageHandler import MessageHandler
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberClient:
    def __init__(self, subscriber_strategy: SubscriberStrategy):
        self._subscriber_strategy: SubscriberStrategy = subscriber_strategy

    def set_strategy(self, subscriber_strategy: SubscriberStrategy):
        self._subscriber_strategy = subscriber_strategy

    def subscribe(self, topic: str, handlers: list[MessageHandler]):
        self._subscriber_strategy.subscribe(topic, handlers)

    def unsubscribe(self, topic: str) -> None:
        self._subscriber_strategy.unsubscribe(topic)
