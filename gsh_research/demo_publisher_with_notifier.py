import zmqmw as zmw
import argparse
from random import randint
from time import sleep
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("brokeraddress", help="IP Address of broker", default="localhost", nargs='?')
    parser.add_argument('brokerport', help="port of the broker", default="5263", type=int, nargs='?')
    args = parser.parse_args()

    broker = zmw.Broker(address=args.brokeraddress, port=args.brokerport, brokertype=zmw.Broker.BrokerType.notifier)
    pub = zmw.Publisher(address=zmw.Address("*", 7777))

    zmw.Publisher.register_publisher(broker, "10.0.0.2", 7777, ['test_topic']) 
    pub.register_topic('test_topic')

    while True:
        pub.publish("test_topic", str(time.time()))
        time.sleep(0.25)


