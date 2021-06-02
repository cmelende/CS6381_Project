import zmq

from merged.middleware.strategy.BrokerStrategy import BrokerStrategy
from hashlib import sha1
import logging
import json

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)


class BrokerNotifierStrategy(BrokerStrategy):

    def close(self) -> None:
        pass

    def __init__(self, port: str) -> None:
        self.reply = self.context.socket(zmq.REP)
        self.publishers = {}
        self.port = port
        self.context = zmq.Context().instance()

    def __register_publisher(self, ip, port, topics=[]):
        self.id = sha1(bytes(f"{ip}:{port}", encoding='utf-8')).hexdigest()
        self.publishers[self.id] = {
            "ip": ip,
            "port": port,
            "topics": topics
        }

    def __get_publishers(self) -> str:
        return json.dumps(self.publishers, indent=4)

    def run(self):
        self.reply.bind(f"tcp://*:{self.port}")
        while True:
            msg = str(self.reply.recv(), encoding='utf-8')
            log.info(f"msg = {msg}")
            if msg == "request":
                self.reply.send_string(self.__get_publishers())
            elif msg.startswith("register$"):
                j = msg.split("$")[1]
                j = json.loads(j)
                self.__register_publisher(ip=j['ip'], port=j['port'], topics=j['topics'] or [])
                self.reply.send_json(j)
