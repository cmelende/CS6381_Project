import sys

from zmqmw.examples.misc.app.App import App
from zmqmw.examples.misc.app.SubscriberApp import SubscriberApp
from zmqmw.examples.misc.app.options.SubscriberAppOptions import SubscriberAppOptions
from zmqmw.examples.misc.handlers.MoviesMessageHandler import MoviesMessageHandler
from zmqmw.examples.misc.handlers.NewsMessageHandler import NewsMessageHandler
from zmqmw.examples.misc.handlers.SportsMessageHandler import SportsMessageHandler
from zmqmw.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from zmqmw.examples.misc.value_objects.TopicHandlers import TopicHandler
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.adapter.SubscriberClient import SubscriberClient

broker_info = BrokerInfo("127.0.0.1", "5560")
broker_xpub_port = "5559"

topic_handlers = [
    TopicHandler("SPORTS", [SportsMessageHandler()]),
    TopicHandler("MOVIES", [MoviesMessageHandler()]),
    TopicHandler("NEWS", [NewsMessageHandler()]),
]


def main(argv):
    options = SubscriberAppOptions(broker_info, broker_xpub_port, argv, topic_handlers, DateTimeConsoleLogger())
    subscriber_app: App[SubscriberClient] = SubscriberApp(options)
    client: SubscriberClient = subscriber_app.create_client()

    try:
        client.listen()
    except KeyboardInterrupt:
        print("Closing down")
        client.close()


if __name__ == "__main__":
    main(sys.argv[1:])
