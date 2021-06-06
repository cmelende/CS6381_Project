from zmqmw.examples.misc.app.options.AppOptions import AppOptions
from zmqmw.examples.misc.logger.Logger import Logger
from zmqmw.examples.misc.value_objects import TopicHandlers
from zmqmw.middleware.BrokerInfo import BrokerInfo


class SubscriberAppOptions(AppOptions):
    def __init__(self,
                 broker_info: BrokerInfo,
                 broker_xpub_port: str,
                 argv,
                 topic_handlers: list[TopicHandlers],
                 logger: Logger):

        super().__init__(broker_info, argv, logger)
        self.BrokerXPubPort = broker_xpub_port
        self.TopicHandlers: list[TopicHandlers] = topic_handlers
