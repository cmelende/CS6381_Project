from zmqmw.base_classes.Logger import Logger
from zmqmw.implementations.notifier.broker.BrokerNotifierStrategy import BrokerNotifierStrategy
from zmqmw.middleware.adapter.BrokerClient import BrokerClient
from zmqmw.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy


# This class can be used as an optional arguement to BrokerProxyStrategy
# to define how things should be logged.
class PrintLogger(Logger):
    def log(self, value: str):
        print(value)


broker = BrokerNotifierStrategy(broker_address="127.0.0.1",
                                broker_port=6000,
                                logger=PrintLogger())

proxy = BrokerClient(broker)

try:
    # this command is blocking - so we catch keyboard interrupts
    proxy.run()
except KeyboardInterrupt:
    proxy.close()
