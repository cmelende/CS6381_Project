import zmq

from merged.base_classes.Logger import Logger
from merged.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerProxyStrategy(BrokerStrategy):
    def __init__(self, broker_address: str, broker_xsub_port: int, broker_xpub_port: int, logger: Logger = None):
        """
        Creates a new brokerProxyStrategy object.

        :param broker_address: The address on which the broker shall be bound.
        :param broker_xsub_port: The port which shall listen for subscribers.
        :param broker_xpub_port: The port which shall listen for publishers.
        :param logger: An optional Log object that implements `merged.base_classes.Logger`
        """

        # let's allow logger to be optional but still available.
        if not logger:
            class NonLogger(Logger):
                def log(self, val: str):
                    pass
            logger = NonLogger()

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
