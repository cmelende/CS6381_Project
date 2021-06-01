from Merged.Middleware.Handler.MessageHandler import MessageHandler
from Merged.Middleware.Strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberProxyStrategy(SubscriberStrategy):
    def unsubscribe(self, topic: str) -> None:
        pass

    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        pass
