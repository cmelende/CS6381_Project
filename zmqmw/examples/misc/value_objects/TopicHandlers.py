from zmqmw.middleware.handler.MessageHandler import MessageHandler


class TopicHandler:
    def __init__(self, topic: str, handler: list[MessageHandler]):
        self.Topic: str = topic
        self.Handlers: list[MessageHandler] = handler
