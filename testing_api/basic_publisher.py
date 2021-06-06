from time import time, sleep
from merged.implementations.proxy.publisher.PublisherProxyStrategy import PublisherProxyStrategy
from merged.middleware.BrokerInfo import BrokerInfo
from merged.middleware.adapter.PublisherClient import PublisherClient


# we create an OPTIONAL logger, for demonstration purposes
class LocalLogger:
    def log(self, val: str):
        print(val)


# notify the code where our broker lives...
broker = BrokerInfo(broker_address="127.0.0.1", broker_sub_port=7000)

# select the strategy under which our broker is running (e.g. proxy or notifier)
strategy = PublisherProxyStrategy(broker_info=broker, logger=LocalLogger())

# create a publisher for the broker...
publisher = PublisherClient(strategy=strategy)

# register topics we want to publish for...
publisher.register(topics=['timer'])

for i in range(100):
    # publish!
    publisher.publish(topic='timer', val=str(time()))
    sleep(1)
