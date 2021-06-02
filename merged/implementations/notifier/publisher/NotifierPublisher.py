import zmq


class NotifierPublisher:
    def __init__(self):
        self.publisher_socket = zmq.Context().instance().socket(zmq.PUB)

    def connect(self, publisher_address: str, publisher_port: str) -> None:
        self.publisher_socket.bind(f"tcp://{publisher_address}:{publisher_port}")

    def publish(self, topic: str, value: str) -> None:
        self.publisher_socket.send_string(f'{topic}:{value}')

    def close(self):
        self.publisher_socket.close()
