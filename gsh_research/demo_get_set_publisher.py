"""
This code requires a broker (notifier) be running.
"""

import zmqmw as zmw
import json

if __name__ == "__main__":
    # instantiate a broker object...
    broker = zmw.Broker(address="localhost", port=5263, brokertype=zmw.Broker.BrokerType.notifier)

    # what publishers are available?
    publishers = str(zmw.Subscriber.get_publishers(broker=broker), encoding='utf-8')
    print(json.loads(publishers))

    # now let's register a publisher
    print(zmw.Publisher.register_publisher(broker, 'localhost', 1234, ['test_topic', 'beta_topic']))

    # now let's see what publishers are available?
    publishers = str(zmw.Subscriber.get_publishers(broker=broker), encoding='utf-8')
    print(json.loads(publishers))

