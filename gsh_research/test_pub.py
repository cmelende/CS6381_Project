import zmqmw as zmw
import logging
from random import randint
from time import sleep
import argparse
import time

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="name of your topic.", default="TOPIC")
    parser.add_argument("count", help="Number of messages to send", type=int, default=5)
    parser.add_argument('sleep', help='time to sleep between messages in milliseconds.', default=1, type=int)
    args = parser.parse_args()

    pub = zmw.Publisher(address=zmw.Address("*", 5263))

    # need to register ourselves with the broker
    pub.register_topic(args.topic)

    count = args.count

    while count > 0:
        pub.publish(args.topic, str(time.time()))
        time.sleep(args.sleep / 1000)
        count -= 1

    pub.unregister_topic("topic1")
    pub.unregister_topic("topic2")

