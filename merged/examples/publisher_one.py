import sys
from time import sleep

from merged.examples.misc.app.App import App
from merged.examples.misc.app.PublisherApp import PublisherApp
from merged.examples.misc.app.options.PublisherAppOptions import PublisherAppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.examples.misc.value_objects.PublisherTopics import PublisherTopics
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.PublisherInfo import PublisherInfo
from merged.middleware.adapter.PublisherClient import PublisherClient

ports = list(map(str, range(5000, 5500)))
broker_info = BrokerInfo("127.0.0.1", "5560")
publisher_info = PublisherInfo("127.0.0.1", ports)
publisher_topics: list[PublisherTopics] = [
    PublisherTopics(["SPORTS", "NEWS"]),
    PublisherTopics(["MOVIES"])
]


def main(argv) -> None:
    options: PublisherAppOptions = PublisherAppOptions(broker_info,
                                                       publisher_info,
                                                       argv,
                                                       DateTimeConsoleLogger(),
                                                       publisher_topics)
    app: App[PublisherClient] = PublisherApp(options)
    client = app.create_client()

    should_continue = True
    while should_continue:
        try:
            sleep(5)
            client.publish("SPORTS", "baseball")
            client.publish("MOVIES", "early showing for dune")
            client.publish("NEWS", "cat rescued from tree")
        except KeyboardInterrupt:
            print("Closing down...")
            client.close()
            should_continue = False


if __name__ == "__main__":
    main(sys.argv[1:])
