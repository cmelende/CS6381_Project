import zmq

from merged.middleware.handler.MessageHandler import MessageHandler
from merged.middleware.handler.NullMessageHandler import NullMessageHandler


class Subscriber:
    def __init__(self, topic: str):
        context = zmq.Context.instance()
        self._subscriber_socket = context.socket(zmq.SUB)
        self.Topic = topic
        self._keep_running = True
        self.__message_handler: list[MessageHandler] = [NullMessageHandler()]

    # todo: probably can make subclasses instead of connecting here
    def connect(self, host_address: str, port: str):
        self._subscriber_socket.connect("tcp://{}:{}".format(host_address, port))
        self._subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, self.Topic)

    def set_handler(self, handler: MessageHandler):
        self.__message_handler: MessageHandler = handler

    def receive(self) -> None:
        msg = self._subscriber_socket.recv()
        handler: MessageHandler
        for handler in self.__message_handler:
            if handler is not NullMessageHandler:
                handler.handle_message(f'{msg}')

    def close(self):
        self._subscriber_socket.close()
