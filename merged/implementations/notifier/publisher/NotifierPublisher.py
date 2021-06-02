import zmq


class NotifierPublisher:
    def __init__(self, publisher_address: str, publisher_port: str, topics: list[str]):
        self.Topics = topics
        self.ctx = zmq.Context().instance()
        self.publisher_socket = self.ctx.socket(zmq.PUB)
        self.publisher_socket.bind(f"tcp://{publisher_address}:{publisher_port}")

    def publish(self, topic: str, value: str):
        if topic in self.Topics:
            self.publisher_socket.send_string(f'{topic}:{value}')

    def close(self):
        self.publisher_socket.close()
