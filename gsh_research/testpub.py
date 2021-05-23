from typing import Callable
import zmq
import logging
from random import randint
from time import sleep
import argparse
import time

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

class TestPublisher:
    def __init__(self, topic="TOPIC", count=5, sleep=1) -> None:
        log.info("In TestPublisher init")
        self.topic = topic
        self.count = count
        self.sleep = sleep
        self.ctx = zmq.Context()
    
    def start(self):
        s = self.ctx.socket(zmq.PUB)
        s.connect("tcp://localhost:5263")
        log.info("Sending messages...")
        for i in range(self.count):
            s.send_string(f'{self.topic}:{time.time()}')
            sleep(self.sleep / 1000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="name of your topic.", default="TOPIC")
    parser.add_argument("count", help="Number of messages to send", type=int, default=5)
    parser.add_argument('sleep', help='time to sleep between messages in milliseconds.', default=1, type=int)
    args = parser.parse_args()

    pub = TestPublisher(topic=args.topic, count=args.count, sleep=args.sleep)
    try:
        pub.start()
    except KeyboardInterrupt:
        pass