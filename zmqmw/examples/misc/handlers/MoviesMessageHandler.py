from datetime import datetime

from zmqmw.middleware.handler.MessageHandler import MessageHandler


class MoviesMessageHandler(MessageHandler):

    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} : '
              f'movies topic handled with message {value}')
