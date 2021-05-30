import zmq

from cmelende_research.N0mq.Broker.pub.Publisher import Publisher
from cmelende_research.N0mq.Broker.pub.TopicsPublisherPair import TopicsPublisherPair


class PublisherContainer:
    def __init__(self, host_address: str, port: str):
        self._context = zmq.Context().instance()
        self._port = port
        self._host_address = host_address
        self._topicsPublisherPairs: list[TopicsPublisherPair] = list[TopicsPublisherPair]()

    def register_pub(self, topics: list[str]) -> None:
        pub = Publisher()
        topics_pub_pair = TopicsPublisherPair(topics, pub)
        pub.connect(self._host_address, self._port)
        self._topicsPublisherPairs.append(topics_pub_pair)

    def publish(self, topic: str, value: str) -> None:
        for topics_publisher_pair in self._topicsPublisherPairs:
            for publisher_topic in topics_publisher_pair.Topics:
                if publisher_topic == topic:
                    topics_publisher_pair.Publisher.publish(topic, value)

    def close(self):
        for pub in self._topicsPublisherPairs:
            pub.Publisher.close()
        self._context.term()
