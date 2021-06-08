import zmq

from zmqmw.base_classes.Logger import Logger
from zmqmw.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerProxyStrategy(BrokerStrategy):
    def __init__(self, broker_address: str, broker_xsub_port: int, broker_xpub_port: int, logger: Logger = Logger()):
        """
        Creates a new brokerProxyStrategy object.

        :param broker_address: The address on which the broker shall be bound.
        :param broker_xsub_port: The port which shall listen for subscribers.
        :param broker_xpub_port: The port which shall listen for publishers.
        :param logger: An optional Log object that implements `zmqmw.base_classes.Logger`
        """

        super().__init__(logger)
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

    def run(self) -> None:
        """
        This method begins the proxying.
        :return: None
        """
        self.__proxy = zmq.proxy(self.__xpub_socket, self.__xsub_socket)

    def close(self) -> None:
        """
        Terminates the Proxy.
        :return: None
        """
        self.__logger.log("Terminating proxy.")
        self.__xpub_socket.close()
        self.__xsub_socket.close()
        self.__context.term()
