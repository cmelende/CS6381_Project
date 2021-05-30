import zmq

from N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase
from N0mq.Broker.handler.NullMessageHandler import NullMessageHandler


class Subscriber:
    def __init__(self, topic: str):
        context = zmq.Context.instance()
        self._subscriber_socket = context.socket(zmq.SUB)
        self.Topic = topic
        self._keep_running = True
        self._message_handler: MessageHandlerBase = NullMessageHandler()

    # todo: probably can make subclasses instead of connecting here
    def connect(self, host_address: str, port: str):
        self._subscriber_socket.connect("tcp://{}:{}".format(host_address, port))
        self._subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, self.Topic)

    def set_handler(self, handler: MessageHandlerBase):
        self._message_handler: MessageHandlerBase = handler

    def receive(self) -> None:
        while self._keep_running:
            msg = self._subscriber_socket.recv()
            if self._message_handler is not NullMessageHandler:
                self._message_handler.handle_message(f'{msg}')

    def close(self):
        self._keep_running = False
        self._subscriber_socket.close()


