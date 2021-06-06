from merged.base_classes.Logger import Logger
from merged.middleware.adapter.BrokerClient import BrokerClient
from merged.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy
import argparse


# This class can be used as an optional arguement to BrokerProxyStrategy
# to define how things should be logged.
class PrintLogger(Logger):
    def log(self, value: str):
        pass #print(value)


def main(args):
    broker = BrokerProxyStrategy(broker_address=args.broker_address,
                                 broker_xpub_port=args.pub_port,
                                 broker_xsub_port=args.sub_port,
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
    parser.add_argument('-sp', '--sub_port', help="Port for subscriber", default=7000, type=int, nargs='?')
    parser.add_argument('-pp', '--pub_port', help="Port for publishers", default=6000, type=int, nargs='?')
    args = parser.parse_args()
    main(args)
