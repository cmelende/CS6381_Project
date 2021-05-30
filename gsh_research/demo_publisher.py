import zmqmw as zmw
import logging
from random import randint
from time import sleep
import time

if __name__ == "__main__":
    pub = zmw.Publisher(address=zmw.Address("*", 5263))

    pub.register_topic(args.topic)

    count = args.count

    while count > 0:
        pub.publish(args.topic, str(time.time()))
        time.sleep(args.sleep / 1000)
        count -= 1

    pub.unregister_topic("topic1")
    pub.unregister_topic("topic2")

