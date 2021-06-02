from merged.implementations.proxy.publisher.ProxyPublisher import ProxyPublisher


class TopicsPublisherPair:
    def __init__(self, topics: list[str], publisher: ProxyPublisher):
        self.Topics: list[str] = topics
        self.Publisher: ProxyPublisher = publisher
