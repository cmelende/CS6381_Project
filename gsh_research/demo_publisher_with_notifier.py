import zmqmw as zmw
import logging
from random import randint
from time import sleep
import time

if __name__ == "__main__":

    broker = zmw.Broker(address="localhost", port=5263, brokertype=zmw.Broker.BrokerType.notifier)
    pub = zmw.Publisher(address=zmw.Address("*", 7777))

    zmw.Publisher.register_publisher(broker, "localhost", 7777, ['test_topic']) 
    pub.register_topic('test_topic')

    while True:
        pub.publish("test_topic", str(time.time()))
        time.sleep(0.25)


