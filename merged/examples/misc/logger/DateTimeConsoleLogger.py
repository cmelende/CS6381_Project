from datetime import datetime

from merged.examples.misc.logger.Logger import Logger


class DateTimeConsoleLogger(Logger):
    def log(self, val: str):
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} : {val}')