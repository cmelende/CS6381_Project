import threading
from datetime import datetime

from cmelende_research.N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase


class TodaysWeatherMessageHandler(MessageHandlerBase):
    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} on thread {threading.current_thread().ident}: '
              f'today\'s weather topic handled with message {value}')
