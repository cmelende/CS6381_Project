from N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase
from datetime import datetime


class SportsTopicMessageHandler(MessageHandlerBase):

    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} : '
              f'sports stats topic handled with message {value}')
