from datetime import datetime

from N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase


class TodaysWeatherMessageHandler(MessageHandlerBase):
    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} : '
              f'today\'s weather topic handled with message {value}')
