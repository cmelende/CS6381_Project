from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.examples.misc.logger.Logger import Logger
from merged.examples.misc.value_objects import TopicHandlers


class SubscriberAppOptions(AppOptions):
    def __init__(self,
                 argv,
                 topic_handlers: list[TopicHandlers],
                 short_options: str,
                 long_options: list[str],
                 logger: Logger):

        super().__init__(argv, short_options, long_options, logger)
        self.TopicHandlers: list[TopicHandlers] = topic_handlers
