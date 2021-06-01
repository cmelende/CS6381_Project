from merged.middleware.handler.MessageHandler import MessageHandler
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberNotifierStrategy(SubscriberStrategy):
    def unsubscribe(self, topic: str) -> None:
        pass

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        pass
