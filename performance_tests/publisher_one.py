import sys
import os

cd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cd)
sys.path.append(pd)

import argparse

from time import sleep, time
from merged.examples.misc.app.App import App
from merged.examples.misc.app.PublisherApp import PublisherApp
from merged.examples.misc.app.options.PublisherAppOptions import PublisherAppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.examples.misc.value_objects.PublisherTopics import PublisherTopics
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.PublisherInfo import PublisherInfo
from merged.middleware.adapter.PublisherClient import PublisherClient


def main(args) -> None:
    broker_info = BrokerInfo(args.broker_address, args.broker_port)
    publisher_info = PublisherInfo(args.publisher_address, [args.publisher_port])
    publisher_topics: list[PublisherTopics] = [
        PublisherTopics(["timer"])
    ]

    options: PublisherAppOptions = PublisherAppOptions(broker_info,
                                                       publisher_info,
                                                       f"--flag={args.mode}",
                                                       DateTimeConsoleLogger(),
                                                       publisher_topics)
    app: App[PublisherClient] = PublisherApp(options)
    client = app.create_client()

    count = args.count
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
    parser = argparse.ArgumentParser()
    parser.add_argument("broker_address", help="IP Address of broker", default="127.0.0.1")
    parser.add_argument('broker_port', help="port of the broker", default=5263, type=int)
    parser.add_argument('publisher_address', help="address of *this* publisher", default="127.0.0.1", type=str)
    parser.add_argument('publisher_port', help="port of *this* publisher's port", default=7000, type=int)
    parser.add_argument('count', help="Number of publications", default=100, type=int)
    parser.add_argument('mode', help="proxy OR notifier", default="proxy", type=str, nargs='?')
    args = parser.parse_args()
    main(args)
