import json
from hashlib import sha1

import zmq

from zmqmw.examples.misc.logger.Logger import Logger
from zmqmw.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerNotifierStrategy(BrokerStrategy):
    def __init__(self, broker_address: str, broker_port: str, logger: Logger) -> None:
        super().__init__(logger)
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

    def __get_publisher_by_topic(self, topic: str) -> str:
        ret_publishers = {}
        for key, value in self.__publishers.items():
            if topic in value['topics']:
                ret_publishers[key] = value
        return json.dumps(ret_publishers, indent=4)

    def run(self):
        url = f'{self.__broker_address}:{self.__broker_port}'
        self.__reply_socket.bind(f'tcp://{url}')
        self._logger.log(f'Started REP socket on {url}')

        while True:
            msg = str(self.__reply_socket.recv(), encoding='utf-8')
            if msg.startswith("request"):
                topic = msg.split("$")[1]
                retrieved_publishers = self.__get_publisher_by_topic(topic)
                self.__reply_socket.send_string(retrieved_publishers)
                self._log_req_reply(msg, url, retrieved_publishers)
            elif msg.startswith("register$"):
                j = msg.split("$")[1]
                j = json.loads(j)
                self.__register_publisher(ip=j['ip'], port=j['port'], topics=j['topics'] or [])
                self.__reply_socket.send_json(j)
                self._log_req_reply("register$", url, j)

    def close(self) -> None:
        self.__reply_socket.close()
        self.__ctx.term()
