from zmqmw.examples.misc.logger.Logger import Logger
from zmqmw.middleware.BrokerInfo import BrokerInfo


class AppOptions:
    def __init__(self, broker_info: BrokerInfo, argv, logger: Logger):
        self.Logger = logger
        self.Argv = argv
        self.BrokerInfo: BrokerInfo = broker_info
