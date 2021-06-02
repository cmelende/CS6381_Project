from abc import ABC, abstractmethod

from merged.examples.misc.logger.Logger import Logger


class BrokerStrategy(ABC):
    def __init__(self, logger: Logger):
        self._logger = logger

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def _log_req_reply(self, req_msg: str, url: str, payload: str):
        self._logger.log(f'responding to request {req_msg} on socket {url} with payload: {payload}')
