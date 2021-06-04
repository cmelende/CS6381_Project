import sys
import os

cd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cd)
sys.path.append(pd)

import argparse
from uuid import uuid4
from merged.examples.misc.app.App import App
from merged.examples.misc.app.SubscriberApp import SubscriberApp
from merged.examples.misc.app.options.SubscriberAppOptions import SubscriberAppOptions
from merged.examples.misc.handlers.PerfMessageHandler import PerfMessageHandler
from merged.examples.misc.logger.DateTimeConsoleLogger import DateTimeConsoleLogger
from merged.examples.misc.value_objects.TopicHandlers import TopicHandler
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.adapter.SubscriberClient import SubscriberClient


def main(args):
    broker_info = BrokerInfo(args.broker_address, args.broker_sub_port)
    broker_xpub_port = args.broker_pub_port
    print(os.path.join(args.directory, f"{args.subscriber_name}"))
    handler = PerfMessageHandler(f"{args.subscriber_name}")
    topic_handlers = [TopicHandler("timer", [handler])]

    options = SubscriberAppOptions(broker_info, broker_xpub_port, f"--flag={args.mode}", topic_handlers, DateTimeConsoleLogger())
    subscriber_app: App[SubscriberClient] = SubscriberApp(options)
    client: SubscriberClient = subscriber_app.create_client()

    try:
        client.listen(expected_count=args.count)
    except KeyboardInterrupt:
        print("Closing down")
        client.close()
    handler.flush()  # used to write messages to log file when perf testing


if __name__ == "__main__":
    cd = os.path.dirname(os.path.realpath(__file__))
    pd = os.path.dirname(cd)
    sys.path.append(pd)

    parser = argparse.ArgumentParser()
    parser.add_argument("broker_address", help="IP Address of broker", default="127.0.0.1")
    parser.add_argument('broker_pub_port', help="publication port of the broker", default=5263, type=int)
    parser.add_argument('broker_sub_port', help="subscriber port of the broker", default=5262, type=int)
    parser.add_argument('count', help="expected items", default=100, type=int)
    parser.add_argument('directory', help="directory to store stats", default="/tmp", type=str)
    parser.add_argument('subscriber_name', help="name of subscriber (for logging)", default=str(uuid4()), type=str)
    parser.add_argument('mode', help="proxy OR notifier", default="proxy", type=str, nargs='?')
    args = parser.parse_args()
    main(args)
