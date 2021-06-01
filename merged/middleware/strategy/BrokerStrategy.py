from abc import ABC, abstractmethod


class BrokerStrategy(ABC):

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
