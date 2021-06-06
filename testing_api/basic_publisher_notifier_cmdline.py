from time import time, sleep
import argparse
from zmqmw.implementations.notifier.publisher.PublisherNotifierStrategy import PublisherNotifierStrategy
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.PublisherInfo import PublisherInfo
from zmqmw.middleware.adapter.PublisherClient import PublisherClient


# we create an OPTIONAL logger, for demonstration purposes
class LocalLogger:
    def log(self, val: str):
        print(val)


def main(args):
    # notify the code where our broker lives...
    broker = BrokerInfo(broker_address=args.broker_address, broker_sub_port=args.broker_port)

    pub_info = PublisherInfo(publisher_address=args.pub_address, publisher_port=args.pub_port)

    # select the strategy under which our broker is running (e.g. proxy or notifier)
    strategy = PublisherNotifierStrategy(broker_info=broker, publisher_info=pub_info, logger=LocalLogger())

    # create a publisher for the broker...
    publisher = PublisherClient(strategy=strategy)

    # register topics we want to publish for...
    publisher.register(topics=['timer'])

    try:
        for i in range(100):
            # publish!
            publisher.publish(topic='timer', val=str(time()))
            sleep(1)
    except KeyboardInterrupt:
        publisher.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ba', "--broker_address", help="IP Address of broker", default="127.0.0.1", type=str,
                        nargs='?')
    parser.add_argument('-bp', '--broker_port', help="Broker info port", default=6000, type=int, nargs='?')
    parser.add_argument('-pa', '--pub_address', help="Address of publisher", default="127.0.0.1", type=str, nargs='?')
    parser.add_argument('-pp', '--pub_port', help="The port we will publish on", default=7000, type=int, nargs='?')
    args = parser.parse_args()
    main(args)
