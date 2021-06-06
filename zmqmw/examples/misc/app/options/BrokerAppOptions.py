from zmqmw.examples.misc.app.options.AppOptions import AppOptions
from zmqmw.examples.misc.logger.Logger import Logger
from zmqmw.middleware.BrokerInfo import BrokerInfo


class BrokerAppOptions(AppOptions):
    def __init__(self, broker_info: BrokerInfo, xpub_port: str, argv, logger: Logger):
        super().__init__(broker_info, argv, logger)
        self.BrokerXSubPort: str = broker_info.BrokerPort
        self.BrokerXPubPort: str = xpub_port
