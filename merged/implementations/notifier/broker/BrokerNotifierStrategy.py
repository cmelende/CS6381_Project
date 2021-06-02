import json
from hashlib import sha1

import zmq

from merged.examples.misc.logger.Logger import Logger
from merged.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerNotifierStrategy(BrokerStrategy):
    def __init__(self, broker_address: str, broker_port: str, logger: Logger) -> None:
        self.__logger = logger
        self.__ctx = zmq.Context().instance()
        self.__reply_socket = self.__ctx.socket(zmq.REP)
        self.__broker_address = broker_address
        self.__publishers = {}
        self.__broker_port = broker_port

    def __register_publisher(self, ip, port, topics=[]):
        self.id = sha1(bytes(f"{ip}:{port}", encoding='utf-8')).hexdigest()
        self.__publishers[self.id] = {
            "ip": ip,
            "port": port,
            "topics": topics
        }

    def __get_publishers(self) -> str:
        return json.dumps(self.__publishers, indent=4)

    def run(self):
        url = f'{self.__broker_address}:{self.__broker_port}'
        self.__reply_socket.bind(f'tcp://{url}')
        self.__logger.log(f'Started REP socket on {url}')

        while True:
            msg = str(self.__reply_socket.recv(), encoding='utf-8')
            if msg == "request":
                self.__reply_socket.send_string(self.__get_publishers())
            elif msg.startswith("register$"):
                j = msg.split("$")[1]
                j = json.loads(j)
                self.__register_publisher(ip=j['ip'], port=j['port'], topics=j['topics'] or [])
                self.__reply_socket.send_json(j)

    def close(self) -> None:
        self.__reply_socket.close()
