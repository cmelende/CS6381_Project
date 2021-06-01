from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.examples.misc.logger.Logger import Logger
from merged.examples.misc.value_objects import TopicHandlers


class SubscriberAppOptions(AppOptions):
    def __init__(self,
                 host: str,
                 port: str,
                 argv,
                 topic_handlers: list[TopicHandlers],
                 logger: Logger):

        super().__init__(host, port, argv, logger)
        self.TopicHandlers: list[TopicHandlers] = topic_handlers
