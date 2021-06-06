from abc import ABC, abstractmethod

from zmqmw.examples.misc.logger.Logger import Logger
from zmqmw.middleware.handler.MessageHandler import MessageHandler


class SubscriberStrategy(ABC):
    def __init__(self, logger: Logger):
        self._logger = logger

    # this doenst really work when we are subscribing to all published topics, for the notifier, to
    # get this to work, we probably want to ask the broker if there are any publishers for that topic
    # then subscribe to those. shouldnt be too hard, just a little more work. But since we arent calling
    # subscribe from any where we only
    @abstractmethod
    def subscribe(self, topic: str, handlers: list[MessageHandler]) -> None: pass

    @abstractmethod
    def unsubscribe(self, topic: str) -> None: pass

    @abstractmethod
    def listen(self, expected_count=None) -> None: pass

    @abstractmethod
    def close(self) -> None: pass

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
