from Merged.Middleware.Strategy.PublisherStrategy import PublisherStrategy


class PublisherNotifierStrategy(PublisherStrategy):
    def register(self, topics: list[str]):
        pass

    def publish(self, topic: str, value: str) -> None:
        pass
