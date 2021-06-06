from abc import ABC, abstractmethod


class MessageHandler(ABC):

    @abstractmethod
    def handle_message(self, value: str) -> None:
        pass
