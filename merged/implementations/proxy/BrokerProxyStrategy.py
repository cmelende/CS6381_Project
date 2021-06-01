import zmq

from merged.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerProxyStrategy(BrokerStrategy):
    def __init__(self, host: str, xsub_port: str, xpub_port: str):
        self.__isRunning = True
        self.__context = zmq.Context().instance()

        self.__pub_socket = self.__context.socket(zmq.XPUB)
        self.__pub_socket.bind(f'tcp://{host}:{xpub_port}')

        self.__sub_socket = self.__context.socket(zmq.SUB)
        self.__sub_socket.bind(f'tcp://{host}:{xsub_port}')
        self.__proxy: zmq.proxy = None

    def run(self):
        self.__proxy = zmq.proxy(self.__pub_socket, self.__sub_socket)

    def close(self):
        self.__pub_socket.close()
        self.__sub_socket.close()
        self.__context.term()
