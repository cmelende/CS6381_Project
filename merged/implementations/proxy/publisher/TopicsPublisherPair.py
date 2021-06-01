from merged.implementations.proxy.publisher.Publisher import Publisher


class TopicsPublisherPair:
    def __init__(self, topics: list[str], publisher: Publisher):
        self.Topics = topics
        self.Publisher = publisher
