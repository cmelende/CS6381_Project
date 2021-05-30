from N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase


class NullMessageHandler(MessageHandlerBase):
    def handle_message(self, value: str) -> None:
        pass
