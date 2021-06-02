import zmq

from merged.examples.misc.logger.Logger import Logger
from merged.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerProxyStrategy(BrokerStrategy):
    def __init__(self, broker_address: str, broker_xsub_port: str, broker_xpub_port: str, logger: Logger):
        self.__logger = logger
        self.__isRunning = True
        self.__context = zmq.Context().instance()

        url = f'{broker_address}:{broker_xpub_port}'
        self.__xpub_socket = self.__context.socket(zmq.XPUB)
        self.__xpub_socket.bind(f'tcp://{url}')
        self.__logger.log(f'Started XPUB socket on {url}')

        url = f'{broker_address}:{broker_xsub_port}'
        self.__xsub_socket = self.__context.socket(zmq.XSUB)
        self.__xsub_socket.bind(f'tcp://{url}')
        self.__logger.log(f'Started XSUB socket on {url}')

        self.__proxy: zmq.proxy = None

    def run(self):
        self.__proxy = zmq.proxy(self.__xpub_socket, self.__xsub_socket)

    def close(self):
        self.__xpub_socket.close()
        self.__xsub_socket.close()
        self.__context.term()
