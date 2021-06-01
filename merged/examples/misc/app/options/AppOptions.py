from merged.examples.misc.logger.Logger import Logger


class AppOptions:
    def __init__(self, host: str, port: str, argv, logger: Logger):
        self.Logger = logger
        self.Argv = argv
        self.Port = port
        self.Host = host
