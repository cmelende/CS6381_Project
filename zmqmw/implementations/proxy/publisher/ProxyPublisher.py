import zmq


class ProxyPublisher:
    def __init__(self):
        self._publish_socket = zmq.Context.instance().socket(zmq.PUB)

    def connect(self, broker_address: str, broker_port: str):
        self._publish_socket.connect(f'tcp://{broker_address}:{broker_port}')

    def publish(self, topic: str, value: str) -> None:
        self._publish_socket.send_string(f'{topic}:{value}')

    def close(self):
        self._publish_socket.close()
