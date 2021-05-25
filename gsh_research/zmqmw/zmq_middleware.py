import threading
import zmq
import logging
from uuid import uuid4
import time

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)


class ProxyBroker:
    def __init__(self, s_port=5262, p_port=5263, ip="*"):
        self.s_port = s_port
        self.p_port = p_port
        self.ip = ip
        self.context = zmq.Context()
        self.subscriber = self._subscriber()
        self.publisher = self._publisher()

    def _subscriber(self):
        log.info("initializing subscriber")
        subscriber = self.context.socket(zmq.XPUB)
        subscriber.bind(f"tcp://*:{self.s_port}")
        return subscriber

    def _publisher(self):
        log.info("initializing publisher.")
        publisher = self.context.socket(zmq.XSUB)
        publisher.bind(f"tcp://{self.ip}:{self.p_port}")
        return publisher

    def start(self):
        try:
            zmq.proxy(self.subscriber, self.publisher)
        except KeyboardInterrupt:
            self.context.destroy()


class RegistrationHandler:
    def __init__(self) -> None:
        self.subscribers = []
        self.publishers = []
    
class Subscriber:
    def __init__(self, identifier=None, host="localhost") -> None:
        self.id = identifier if identifier is not None else str(uuid4())
        self.host = host
        self._running = False
        self.t = None
        self.id = None
        self.callbacks = {} 
        log.info("In TestSubscriber init")

        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.SUB)

        self.subscriptions = []

    def _register(self, t):
        print("subscriptions", self.subscriptions)
        if t not in self.subscriptions:
            print(f"adding {t}")
            self.subscriptions.append(t)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, t)

    def _start(self):
        self.running = True
        self.socket.connect(f"tcp://{self.host}:5262")
        print(f"cb = {self.callbacks}")
        while self.running:
            try:
                topic , *body = self.socket.recv_string(zmq.DONTWAIT).split(":")
                if topic in self.callbacks:
                    for cb in self.callbacks[topic]:
                        cb(topic, body)
            except zmq.Again:
                pass

    def register_sub(self, topic):
        log.info(f"register_sub: topic: '{topic}'")
        self._register(topic)
        if not isinstance(self.t, threading.Thread):
            self.t = threading.Thread(target=self._start)
            self.t.start()
         
    def unregister_sub(self, topic):
        if topic != "*":
            self.socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            self.subscriptions.remove(topic)
        else:
            for s in self.subscriptions:
                self.socket.setsockopt_string(zmq.UNSUBSCRIBE, s)
                self.subscriptions.remove(s)
            self.stop()
    
    def stop(self):
        self.running = False
        time.sleep(0.5)
        self.ctx.destroy()

    def notify(self, topic, fn):
        if topic not in self.callbacks:
            self.callbacks[topic] = [fn]
        else:
            self.callbacks[topic].append(fn)

    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, val):
        self._running = val

class Publisher:
    def __init__(self) -> None:
        pass 
    
    def register_pub(self):
        pass 
