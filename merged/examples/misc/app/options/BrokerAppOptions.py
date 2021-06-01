from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.examples.misc.logger.Logger import Logger


class BrokerAppOptions(AppOptions):
    def __init__(self, host: str, xpub_port: str, xsub_port: str, argv, logger: Logger):
        super().__init__(host, argv, logger)
        self.XSubPort = xsub_port
        self.XPubPort = xpub_port
