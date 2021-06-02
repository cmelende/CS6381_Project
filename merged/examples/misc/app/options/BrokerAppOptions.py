from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.examples.misc.logger.Logger import Logger


class BrokerAppOptions(AppOptions):
    def __init__(self, broker_address: str, xpub_port: str, xsub_port: str, argv, logger: Logger):
        super().__init__(broker_address, argv, logger)
        self.BrokerXSubPort: str = xsub_port
        self.BrokerXPubPort: str = xpub_port
