import sys

from merged.examples.misc.app.App import App
from merged.examples.misc.app.SubscriberApp import SubscriberApp
from merged.examples.misc.app.options.SubscriberAppOptions import SubscriberAppOptions
from merged.examples.misc.handlers.MoviesMessageHandler import MoviesMessageHandler
from merged.examples.misc.handlers.NewsMessageHandler import NewsMessageHandler
from merged.examples.misc.handlers.SportsMessageHandler import SportsMessageHandler
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.examples.misc.value_objects.TopicHandlers import TopicHandler
from merged.middleware.adapter.SubscriberClient import SubscriberClient

host = "127.0.0.1"
port = "5560"
topic_handlers = [
    TopicHandler("SPORTS", [SportsMessageHandler()]),
    TopicHandler("MOVIES", [MoviesMessageHandler()]),
    TopicHandler("NEWS", [NewsMessageHandler()])
]


def main(argv):
    options = SubscriberAppOptions(host, port, argv, topic_handlers, DateTimeConsoleLogger())
    subscriber_app: App[SubscriberClient] = SubscriberApp(options)
    client: SubscriberClient = subscriber_app.create_client()

    try:
        client.listen()
    except KeyboardInterrupt:
        print("Closing down")
        client.close()


if __name__ == "__main__":
    main(sys.argv[1:])