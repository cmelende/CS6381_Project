from typing import Callable
import zmq
import logging
import argparse
from random import randint
from time import sleep
from uuid import uuid4
from threading import Thread

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

class TestSubscriber:
    def __init__(self, identifier=None, listen_count=0, topic="") -> None:
        self.id = identifier
        self.topic = topic
        log.info("In TestSubscriber init")
        self.ctx = zmq.Context()
        self.count = -1 if listen_count == 0 else listen_count

    def start(self):
        s = self.ctx.socket(zmq.SUB)
        s.connect("tcp://localhost:5262")
        s.setsockopt_string(zmq.SUBSCRIBE, self.topic)

        log.info(f"thread:{self.id} waiting for message")

        while self.count != 0:
            log.info(f"{self.id} received: {s.recv()}")
            self.count -=1 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="name of your topic.", default="")
    parser.add_argument("count", help="Number of messages to receive (0 = infinite)", type=int, default=100)
    parser.add_argument("threads", help="number of threads to do this.", type=int, default=1)
    args = parser.parse_args()

    subscribers = [TestSubscriber(identifier=str(uuid4()), listen_count=args.count, topic=args.topic) for i in range(args.threads)]
    for s in subscribers:
        t = Thread(target=s.start)
        t.start()

