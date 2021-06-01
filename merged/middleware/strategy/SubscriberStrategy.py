from abc import ABC, abstractmethod

from Merged.Middleware.Handler.MessageHandler import MessageHandler


class SubscriberStrategy(ABC):

    @abstractmethod
    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, topic: str) -> None:
        pass
