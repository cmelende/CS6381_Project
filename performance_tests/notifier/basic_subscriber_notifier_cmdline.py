import argparse
from time import time, sleep
import os
from zmqmw.implementations.notifier.subscriber.SubscriberNotifierStrategy import SubscriberNotifierStrategy
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.adapter.SubscriberClient import SubscriberClient

# we create an OPTIONAL logger, for demonstration purposes
from zmqmw.middleware.handler.MessageHandler import MessageHandler


# an OPTIONAL logger we can use for our strategy
class LocalLogger:
    def log(self, val: str):
        print(val)


# this is used on line 30 to show how we might handle an event...
class TimerHandler(MessageHandler):
    def __init__(self, directory, name):
        self.file = os.path.join(directory, f"{name}.csv")
        self.fd = open(self.file, "a+")
        self.count = 0

    def __del__(self):
        print("Deleting object...")
        try:
            self.fd.close()
        except Exception:
            pass

    def handle_message(self, value: str) -> None:
        print(value)
        topic, msg_id, timestamp = value.split(":")
        timestamp = float(timestamp)
        latency = time() - timestamp
        x = self.fd.write(f"{self.count},{msg_id},{latency}\n")
        self.fd.flush()
        print(f"{self.count},{value} -- written: {x}\n", end='')
        self.count += 1


def main(args):
    # notify the code where our broker lives...
    broker = BrokerInfo(broker_address=args.broker_address, broker_pub_port=args.broker_port)

    # select the strategy under which our broker is running (e.g. proxy or notifier)
    strategy = SubscriberNotifierStrategy(broker_info=broker, logger=LocalLogger())

    # create a publisher for the broker...
    subscriber = SubscriberClient(subscriber_strategy=strategy)

    subscriber.subscribe(topic='timer', handlers=[TimerHandler(args.directory, args.name)])

    try:
        subscriber.listen()
    except KeyboardInterrupt:
        subscriber.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help="Directory to save data", type=str)
    parser.add_argument('-n', '--name', help="subscriber name", type=str)
    parser.add_argument('-ba', "--broker_address", help="IP Address of broker", default="127.0.0.1", type=str,
                        nargs='?')
    parser.add_argument('-bp', '--broker_port', help="Broker info port", default=6000, type=int, nargs='?')
    args = parser.parse_args()
    main(args)
