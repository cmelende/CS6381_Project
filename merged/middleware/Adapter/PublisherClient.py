from merged.middleware.Strategy.PublisherStrategy import PublisherStrategyBase


class PublisherClient:

    def __init__(self, strategy: PublisherStrategyBase):
        self._publisher_strategy: PublisherStrategyBase = strategy

    def set_strategy(self, strategy: PublisherStrategyBase):
        self._publisher_strategy: PublisherStrategyBase = strategy

    def register(self, topics: list[str]) -> None:
        self._publisher_strategy.register(topics)

    def publish(self, topic: str, val: str) -> None:
        self._publisher_strategy.publish(topic, val)
