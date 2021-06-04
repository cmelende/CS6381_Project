import sys
import os

cd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cd)
sys.path.append(pd)

from merged.examples.misc.app.App import App
from merged.examples.misc.app.BrokerApp import BrokerApp
from merged.examples.misc.app.options.BrokerAppOptions import BrokerAppOptions
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.adapter.BrokerClient import BrokerClient
import argparse


def main(args) -> None:
    print("Starting broker...")
    broker_info = BrokerInfo(args.broker_address, args.publisher_port)
    xpub_port = args.subscriber_port

    options: BrokerAppOptions = BrokerAppOptions(broker_info, xpub_port, f'--flag={args.mode}', DateTimeConsoleLogger())
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
    parser = argparse.ArgumentParser()
    parser.add_argument("broker_address", help="IP Address of broker", default="127.0.0.1")
    parser.add_argument('publisher_port', help="port of the broker (xpub)", default="5263", type=int)
    parser.add_argument('subscriber_port', help="port of the broker (xsub)", default="5262", type=int)
    parser.add_argument('mode', help="proxy OR notifier", default="proxy", type=str, nargs='?')
    args = parser.parse_args()
    main(args)
