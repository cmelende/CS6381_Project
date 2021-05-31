import zmq
from datetime import datetime


class Publisher:
    def __init__(self):
        self._publish_socket = zmq.Context.instance().socket(zmq.PUB)

    def connect(self, host_address: str, port: str, direct_connect: bool = False):
        if direct_connect:
            self._publish_socket.bind("tcp://{}:{}".format(host_address, port))
        else:
            self._publish_socket.connect("tcp://{}:{}".format(host_address, port))

    def publish(self, topic: str, value: str) -> None:
        msg = f'{topic} : {value}'
        self._publish_socket.send_string(msg)
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} sent - {msg}')

    def close(self):
        self._publish_socket.close()
