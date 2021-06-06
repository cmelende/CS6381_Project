from zmqmw.examples.misc.app.options.AppOptions import AppOptions
from zmqmw.examples.misc.logger.Logger import Logger
from zmqmw.examples.misc.value_objects.PublisherTopics import PublisherTopics
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.PublisherInfo import PublisherInfo


class PublisherAppOptions(AppOptions):
    def __init__(self,
                 broker_info: BrokerInfo,
                 publisher_info: PublisherInfo,
                 argv,
                 logger: Logger,
                 publisher_topics: list[PublisherTopics]):

        super().__init__(broker_info, argv, logger)
        self.PublisherInfo = publisher_info
        self.PublisherTopics = publisher_topics
