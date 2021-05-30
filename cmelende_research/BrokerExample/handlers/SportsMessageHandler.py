import threading

from N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase
from datetime import datetime


class SportsMessageHandler(MessageHandlerBase):

    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} on thread {threading.current_thread().ident}: '
              f'sports topic handled with message {value}')
