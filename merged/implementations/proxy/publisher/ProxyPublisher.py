import zmq
from datetime import datetime


class ProxyPublisher:
    def __init__(self):
        self._publish_socket = zmq.Context.instance().socket(zmq.PUB)

    def connect(self, broker_address: str, broker_port: str):
        self._publish_socket.connect(f'tcp://{broker_address}:{broker_port}')

    def publish(self, topic: str, value: str) -> None:
        msg = f'{topic} : {value}'
        self._publish_socket.send_string(msg)
        print(f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")} sent - {msg}')

    def close(self):
        self._publish_socket.close()
