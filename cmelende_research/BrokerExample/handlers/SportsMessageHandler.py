from datetime import datetime

from cmelende_research.N0mq.Broker.handler.MessageHandlerBase import MessageHandlerBase


class SportsMessageHandler(MessageHandlerBase):

    def handle_message(self, value: str) -> None:
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} : '
              f'sports topic handled with message {value}')
