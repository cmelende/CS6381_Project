import sys
from time import sleep

from merged.examples.misc.app.App import App
from merged.examples.misc.app.PublisherApp import PublisherApp
from merged.examples.misc.app.options.PublisherAppOptions import PublisherAppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.examples.misc.value_objects.PublisherTopics import PublisherTopics
from merged.middleware.adapter.PublisherClient import PublisherClient

host = "127.0.0.1"
port = "5560"
publisher_topics: list[PublisherTopics] = [
    PublisherTopics(["SPORTS", "NEWS"]),
    PublisherTopics(["WEATHER", "POLITICS"])
]


def main(argv) -> None:
    options: PublisherAppOptions = PublisherAppOptions(host, port, argv, DateTimeConsoleLogger(), publisher_topics)
    app: App[PublisherClient] = PublisherApp(options)
    client = app.create_client()

    should_continue = True
    while should_continue:
        try:
            sleep(5)
            client.publish("SPORTS", "baseball")
            client.publish("WEATHER", "Yankees: 1W-0L")
            client.publish("POLITICS", "Congress in session")
            client.publish("NEWS", "cat rescued from tree")
        except KeyboardInterrupt:
            print("Closing down")
            client.close()
            should_continue = False


if __name__ == "__main__":
    main(sys.argv[1:])
