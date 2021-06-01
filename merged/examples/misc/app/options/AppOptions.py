from merged.examples.misc.logger.Logger import Logger


class AppOptions:
    def __init__(self, argv, short_options: str,
                 long_options: list[str], logger: Logger):
        self.Logger = logger
        self.ShortOptions: str = short_options
        self.LongOptions: list[str] = long_options
        self.Argv = argv
