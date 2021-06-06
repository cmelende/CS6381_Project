from merged.middleware.strategy.PublisherStrategy import PublisherStrategy


class PublisherClient:

    def __init__(self, strategy: PublisherStrategy):
        self._publisher_strategy: PublisherStrategy = strategy

    def set_strategy(self, strategy: PublisherStrategy):
        self._publisher_strategy: PublisherStrategy = strategy

    def register(self, topics: list[str]) -> None:
        """
        Registers a list of topics with the Publisher.

        :param topics: A list of topics for the publisher to register.
        :return: None
        """
        self._publisher_strategy.register(topics)

    def publish(self, topic: str, val: str) -> None:
        self._publisher_strategy.publish(topic, val)

    def close(self):
        self._publisher_strategy.close()
