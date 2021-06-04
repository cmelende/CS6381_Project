import sys
from time import sleep, time

from merged.examples.misc.app.App import App
from merged.examples.misc.app.PublisherApp import PublisherApp
from merged.examples.misc.app.options.PublisherAppOptions import PublisherAppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.examples.misc.value_objects.PublisherTopics import PublisherTopics
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.PublisherInfo import PublisherInfo
from merged.middleware.adapter.PublisherClient import PublisherClient

broker_info = BrokerInfo("127.0.0.1", "5560")
publisher_info = PublisherInfo("127.0.0.1", [7000])
publisher_topics: list[PublisherTopics] = [
    PublisherTopics(["timer"])
]


def main(argv) -> None:
    options: PublisherAppOptions = PublisherAppOptions(broker_info,
                                                       publisher_info,
                                                       argv,
                                                       DateTimeConsoleLogger(),
                                                       publisher_topics)
    app: App[PublisherClient] = PublisherApp(options)
    client = app.create_client()

    count = 100
    while count > 0:
        try:
            sleep(0.10)
            client.publish("timer", str(time()))
            count -= 1
        except KeyboardInterrupt:
            print("Closing down...")
            client.close()
            count = 0


if __name__ == "__main__":
    main(sys.argv[1:])
