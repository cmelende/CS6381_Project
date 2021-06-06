from merged.middleware.handler.MessageHandler import MessageHandler


class NullMessageHandler(MessageHandler):
    def handle_message(self, value: str) -> None:
        pass
