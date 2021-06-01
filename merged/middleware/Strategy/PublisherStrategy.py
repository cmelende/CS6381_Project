from abc import ABC, abstractmethod


class PublisherStrategyBase(ABC):

    @abstractmethod
    def register(self, topics: list[str]):
        pass

    @abstractmethod
    def publish(self, topic: str, value: str) -> None:
        pass
