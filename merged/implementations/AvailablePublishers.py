class AvailablePublishers:
    def __init__(self, host: str, port: str, topics: list[str]):
        self.Topics = topics
        self.Port = port
        self.Host = host
