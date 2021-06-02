import zmq

from merged.middleware.handler.MessageHandler import MessageHandler


class ProxySubscriber:
    def __init__(self, topic: str, handlers: list[MessageHandler]):
        context = zmq.Context().instance()
        self._subscriber_socket = context.socket(zmq.SUB)
        self.Topic = topic
        self._keep_running = True
        self.__message_handlers: list[MessageHandler] = handlers

    def connect(self, broker_address: str, broker_port: str):
        self._subscriber_socket.connect(f'tcp://{broker_address}:{broker_port}')
        self._subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, self.Topic)

    def receive(self) -> None:
        msg = self._subscriber_socket.recv()
        for handler in self.__message_handlers:
            handler.handle_message(f'{msg}')

    def close(self):
        self._subscriber_socket.close()
