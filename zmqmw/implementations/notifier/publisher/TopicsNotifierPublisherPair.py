from zmqmw.implementations.notifier.publisher.NotifierPublisher import NotifierPublisher


class TopicsNotifierPublisherPair:
    def __init__(self, topics: list[str], publisher: NotifierPublisher):
        self.Publisher: NotifierPublisher = publisher
        self.Topics: list[str] = topics
