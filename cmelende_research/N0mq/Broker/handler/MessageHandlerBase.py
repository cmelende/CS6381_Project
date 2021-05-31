from abc import ABC, abstractmethod


class MessageHandlerBase(ABC):

    @abstractmethod
    def handle_message(self, value: str) -> None:
        pass
