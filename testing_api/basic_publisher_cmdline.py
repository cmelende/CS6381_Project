from time import time, sleep
import argparse
from zmqmw.implementations.proxy.publisher.PublisherProxyStrategy import PublisherProxyStrategy
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.adapter.PublisherClient import PublisherClient


# we create an OPTIONAL logger, for demonstration purposes
class LocalLogger:
    def log(self, val: str):
        print(val)


def main(args):
    # notify the code where our broker lives...
    broker = BrokerInfo(broker_address=args.broker_address, broker_sub_port=args.sub_port)

    # select the strategy under which our broker is running (e.g. proxy or notifier)
    strategy = PublisherProxyStrategy(broker_info=broker, logger=LocalLogger())

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
    parser.add_argument('-sp', '--sub_port', help="Port for subscriber", default=7000, type=int, nargs='?')
    args = parser.parse_args()
    main(args)
