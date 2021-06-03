import zmqmw as zmw
import argparse
from random import randint
from time import sleep
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("brokeraddress", help="IP Address of broker", default="localhost", nargs='?')
    parser.add_argument('brokerport', help="port of the broker", default="5263", type=int, nargs='?')
    parser.add_argument('localip', help="the ip of _this_ device.", default='127.0.0.1', nargs='?')
    parser.add_argument('topics', help="comma-separated list of topics (no spaces)", default='test_topic', nargs='?')
    args = parser.parse_args()

    broker = zmw.Broker(address=args.brokeraddress, port=args.brokerport, brokertype=zmw.Broker.BrokerType.notifier)
    pub = zmw.Publisher(address=zmw.Address(args.localip, 7777))
    zmw.Publisher.register_publisher(broker, args.localip, 7777, ['test_topic']) 
    pub.register_topic('test_topic')

    count = 100
    while count > 0:
        pub.publish("test_topic", str(time.time()))
        time.sleep(0.10)
        count -= 1


