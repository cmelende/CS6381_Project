import argparse
from zmqmw.base_classes.Logger import Logger
from zmqmw.implementations.notifier.broker.BrokerNotifierStrategy import BrokerNotifierStrategy
from zmqmw.middleware.adapter.BrokerClient import BrokerClient


# This class can be used as an optional arguement to BrokerProxyStrategy
# to define how things should be logged.
class PrintLogger(Logger):
    def log(self, value: str):
        print(value)


def main(args):
    broker = BrokerNotifierStrategy(broker_address=args.broker_address,
                                    broker_port=args.broker_port,
                                    logger=PrintLogger())

    proxy = BrokerClient(broker)

    try:
        # this command is blocking - so we catch keyboard interrupts
        proxy.run()
    except KeyboardInterrupt:
        proxy.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ba', "--broker_address", help="IP Address of broker", default="127.0.0.1", type=str,
                        nargs='?')
    parser.add_argument('-bp', '--broker_port', help="Broker info port", default=6000, type=int, nargs='?')
    args = parser.parse_args()
    main(args)
