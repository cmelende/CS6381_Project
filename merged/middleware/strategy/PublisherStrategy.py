from abc import ABC, abstractmethod


class PublisherStrategy(ABC):

    @abstractmethod
    def register(self, topics: list[str]) -> None:
        pass

    @abstractmethod
    def publish(self, topic: str, value: str) -> None:
        pass

    @abstractmethod
    def close(self):
        pass

