from merged.base_classes.Logger import Logger
from merged.middleware.adapter.BrokerClient import BrokerClient
from merged.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy


# This class can be used as an optional arguement to BrokerProxyStrategy
# to define how things should be logged.
class PrintLogger(Logger):
    def log(self, value: str):
        print(value)


broker = BrokerProxyStrategy(broker_address="127.0.0.1",
                             broker_xpub_port=6000,
                             broker_xsub_port=7000,
                             logger=PrintLogger())
proxy = BrokerClient(broker)

try:
    # this command is blocking - so we catch keyboard interrupts
    proxy.run()
except KeyboardInterrupt:
    proxy.close()
