from abc import ABC, abstractmethod

from merged.examples.misc.logger.Logger import Logger
from merged.middleware.handler.MessageHandler import MessageHandler


class SubscriberStrategy(ABC):
    def __init__(self, logger: Logger):
        self._logger = logger

    @abstractmethod
    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, topic: str) -> None:
        pass

    @abstractmethod
    def listen(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def _log_subscription(self, address: str, port: str, topic: str, handlers: list[MessageHandler]):
        handler_names = self.__get_message_handler_names(handlers)
        self._logger.log(f'Subscribing to {topic} at {address}:{port} '
                         f'with handlers {",".join(map(str, handler_names))}')

    @staticmethod
    def __get_message_handler_names(handlers: list[MessageHandler]) -> list[str]:
        names: list[str] = list[str]()
        for handle in handlers:
            names.append(type(handle).__name__)
        return names

    def _log_listen(self, topic: str):
        self._logger.log(f'Listening for topic {topic}')
