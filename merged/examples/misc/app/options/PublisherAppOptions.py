from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.examples.misc.logger.Logger import Logger
from merged.examples.misc.value_objects.PublisherTopics import PublisherTopics


class PublisherAppOptions(AppOptions):
    def __init__(self, host: str, port: str, argv, logger: Logger, publisher_topics: list[PublisherTopics]):
        super().__init__(host, argv, logger)
        self.PublisherTopics = publisher_topics
        self.Port = port
