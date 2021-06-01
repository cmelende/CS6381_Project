from abc import ABC, abstractmethod

from merged.middleware.handler.MessageHandler import MessageHandler


class SubscriberStrategy(ABC):

    @abstractmethod
    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, topic: str) -> None:
        pass
