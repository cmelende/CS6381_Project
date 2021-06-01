from Merged.Middleware.Handler.MessageHandler import MessageHandler
from Merged.Middleware.Strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberNotifierStrategy(SubscriberStrategy):
    def unsubscribe(self, topic: str) -> None:
        pass

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        pass
