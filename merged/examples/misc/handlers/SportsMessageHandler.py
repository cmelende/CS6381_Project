from datetime import datetime

from merged.middleware.handler.MessageHandler import MessageHandler


class SportsMessageHandler(MessageHandler):

    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} : '
              f'sports topic handled with message {value}')
