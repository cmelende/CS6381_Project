import threading

from datetime import datetime

from cmelende_research.N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase


class StatsMessageHandler(MessageHandlerBase):

    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} on thread {threading.current_thread().ident}: '
              f'sports stats topic handled with message {value}')
