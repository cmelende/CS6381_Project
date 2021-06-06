from abc import ABC, abstractmethod

from zmqmw.examples.misc.logger.Logger import Logger


class PublisherStrategy(ABC):
    def __init__(self, logger: Logger):
        self._logger = logger

    @abstractmethod
    def register(self, topics: list[str]) -> None:
        pass

    @abstractmethod
    def publish(self, topic: str, value: str) -> None:
        pass

    @abstractmethod
    def close(self):
        pass

    def _log_registration(self, address: str, port: str, topics: list[str], obj):
        self._logger.log(
            f'Registering {type(obj).__name__} to url:'
            f' {address}:{port}'
            f' and to topics {",".join(map(str, topics))}')

    def _log_socket_connection(self, url: str, socket_type: str):
        self._logger.log(f'Connecting {socket_type} socket to {url}')

    def _log_send(self, url: str, payload: str):
        self._logger.log(f'Sending to {url}: {payload}')

    def _log_publish(self, topic: str, value: str):
        self._logger.log(f'publishing topic {topic} with message: {value}')

    def _log_recv(self, url: str, received_string: str):
        self._logger.log(f'received on {url}: {received_string}')
