from abc import ABC, abstractmethod


class BrokerStrategy(ABC):

    @abstractmethod
    def run(self):
        pass
