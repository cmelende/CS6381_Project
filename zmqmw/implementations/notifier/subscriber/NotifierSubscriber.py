import zmq

from zmqmw.middleware.handler.MessageHandler import MessageHandler


class NotifierSubscriber:
    def __init__(self, topic: str, handlers: list[MessageHandler]):
        context = zmq.Context().instance()
        self.Topic = topic
        self.__subscriber_socket = context.socket(zmq.SUB)
        self.__message_handlers: list[MessageHandler] = handlers

    def connect(self, broker_address: str, broker_port: str) -> None:
        self.__subscriber_socket.connect(f'tcp://{broker_address}:{broker_port}')
        self.__subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, self.Topic)

    def receive(self) -> None:
        try:
            msg = self.__subscriber_socket.recv(zmq.DONTWAIT)
            for handler in self.__message_handlers:
                handler.handle_message(f'{msg.decode("utf-8")}')
        except zmq.Again:
            pass

    def close(self) -> None:
        self.__subscriber_socket.close()
