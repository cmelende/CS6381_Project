import sys

from merged.examples.misc.app.App import App
from merged.examples.misc.app.BrokerApp import BrokerApp
from merged.examples.misc.app.options.BrokerAppOptions import BrokerAppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.adapter.BrokerClient import BrokerClient
import argparse


broker_info = BrokerInfo("127.0.0.1", "5560")
xpub_port = "5559"


def main(argv) -> None:
    options: BrokerAppOptions = BrokerAppOptions(broker_info, xpub_port, argv, DateTimeConsoleLogger())
    app: App[BrokerClient] = BrokerApp(options)
    client = app.create_client()

    should_continue = True
    while should_continue:
        try:
            client.run()
        except KeyboardInterrupt:
            print("Closing down")
            client.close()
            should_continue = False


if __name__ == "__main__":
    main(sys.argv[1:])
