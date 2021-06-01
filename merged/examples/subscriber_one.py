import sys

from merged.examples.misc.app.App import App
from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.examples.misc.app.SubscriberApp import SubscriberApp
from merged.examples.misc.value_objects.TopicHandlers import TopicHandler
from merged.examples.misc.handlers.MoviesMessageHandler import MoviesMessageHandler
from merged.examples.misc.handlers.NewsMessageHandler import NewsMessageHandler
from merged.examples.misc.handlers.SportsMessageHandler import SportsMessageHandler
from merged.middleware.adapter.SubscriberClient import SubscriberClient

short_options = "f"
long_options = ["flag"]
topic_handlers = [
    TopicHandler("SPORTS", [SportsMessageHandler()]),
    TopicHandler("MOVIES", [MoviesMessageHandler()]),
    TopicHandler("NEWS", [NewsMessageHandler()])
]


def main(argv):
    options = AppOptions(argv, short_options, long_options, DateTimeConsoleLogger())
    subscriber_app: App[SubscriberClient] = SubscriberApp(options)
    subscriber_app.run()


if __name__ == "__main__":
    main(sys.argv)
