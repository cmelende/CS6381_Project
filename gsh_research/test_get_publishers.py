from json import encoder
"""
This code requires a broker (notifier) be running.
"""

import zmqmw as zmw
import logging
import argparse
import json

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # instantiate a broker object...
    broker = zmw.Broker(address="localhost", port=5263, brokertype=zmw.Broker.BrokerType.notifier)

    # what publishers are available?
    publishers = str(zmw.Subscriber.get_publishers(broker=broker), encoding='utf-8')
    print(json.loads(publishers))

    # now let's register a publisher
    print(str(zmw.Publisher.register_publisher(broker, 'localhost', 1234), encoding='utf-8'))

    # now let's see what publishers are available?
    publishers = str(zmw.Subscriber.get_publishers(broker=broker), encoding='utf-8')
    print(json.loads(publishers))

