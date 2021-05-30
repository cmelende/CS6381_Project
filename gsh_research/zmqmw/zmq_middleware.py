import threading
import zmq
import logging
from uuid import uuid4
import time
from enum import Enum
from hashlib import sha1
import json

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
        log.info("\tProxy Broker Started...")
        log.info(f"\tListening for publisher on port: {p_port}")
        log.info(f"\tListening for subscribers on port: {s_port}")

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

class NotifierBroker:
    def __init__(self, port=5263) -> None:
        self.publishers = {} 
        self.port = port
        self.context = zmq.Context()
    
    def register_publisher(self, ip, port, topics=[]):
        self.id = sha1(bytes(f"{ip}:{port}", encoding='utf-8')).hexdigest()
        self.publishers[self.id] = {
            "ip": ip,
            "port": port,
            "topics": topics
        }
       
    def get_publishers(self):
        return json.dumps(self.publishers, indent=4)
    
    def start(self):
        self.reply = self.context.socket(zmq.REP)
        self.reply.bind(f"tcp://*:{self.port}")
        while True:
            msg = str(self.reply.recv(), encoding='utf-8')
            log.info(f"msg = {msg}")
            if msg == "request":
                self.reply.send_string(self.get_publishers())
            elif msg.startswith("register$"):
                j = msg.split("$")[1]
                j = json.loads(j)
                self.register_publisher(ip=j['ip'], port=j['port'], topics=j['topics'] or [])
                self.reply.send_json(j)

class Address:
    def __init__(self, address, port):
        self.address = address
        self.port = port

class Broker(Address):
    class BrokerType(Enum):
        proxy = 0
        notifier = 1

    def __init__(self, address, port, brokertype: BrokerType):
        super().__init__(address, port)
        self.brokertype = brokertype 

class Subscriber:
    def __init__(self, identifier=None, host="localhost", port=5263) -> None:
        self.id = identifier if identifier is not None else str(uuid4())
        self.host = host
        self.port = port
        self._running = False
        self.t = None
        self.callbacks = {} 
        log.info("In TestSubscriber init")

        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.SUB)

        self.subscriptions = []

    def _register(self, t):
        if t not in self.subscriptions:
            self.subscriptions.append(t)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, t)

    def _start(self):
        self.running = True
        self.socket.connect(f"tcp://{self.host}:{self.port}")
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
        self.t.join()
        self.ctx.destroy()

    def register_notify(self, topic, fn):
        if topic not in self.callbacks:
            self.callbacks[topic] = [fn]
        else:
            self.callbacks[topic].append(fn)
    
    @staticmethod
    def get_publishers(broker):
        ctx = zmq.Context.instance()
        s = ctx.socket(zmq.REQ)
        s.connect(f"tcp://{broker.address}:{broker.port}")
        s.send_string("request")
        return(s.recv())

    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, val):
        self._running = val

class Publisher:
    def __init__(self, address: Address = None, broker: Broker = None) -> None:
        if not address and not broker:
            raise ValueError("Must specify broker or address")

        self.topics = []
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PUB)

        if broker is not None:
            log.info(f"Publisher sending to broker {broker.address}:{broker.port}")
            self.socket.connect(f"tcp://{broker.address}:{broker.port}")
        else:
            log.info("Publisher listening without broker.")
            self.socket.bind(f"tcp://{address.address}:{address.port}")
        self._running = True

    def register_topic(self, topic):
        if topic not in self.topics:
            log.info(f"Topic {topic} registered.")
            self.topics.append(topic)
        else:
            log.warn(f"Topic already added.") 
            return 

    def unregister_topic(self, topic):
        if topic in self.topics:
            self.topics.remove(topic)

    def get_registered_topics(self):
        return self.topics
    
    def publish(self, topic, data):
        if topic in self.topics:
            self.socket.send_string(":".join([topic, data]))
        else:
            log.error("This is an unregistered topic for this publisher.")
    
    @staticmethod
    def register_publisher(broker: Broker, ip, port, topics=[]):
        if broker.brokertype == Broker.BrokerType.notifier:
            ctx = zmq.Context.instance()
            s = ctx.socket(zmq.REQ)
            s.connect(f"tcp://{broker.address}:{broker.port}")
            reg_body = {
                "ip": ip,
                "port": port,
                "topics": topics
            }
            s.send_string(f'register${json.dumps(reg_body)}')
            resp = str(s.recv(), encoding='utf-8')
            log.info(f"registration response:{resp}")
            return resp

    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, newval):
        if isinstance(newval, bool):
            self.running = newval
