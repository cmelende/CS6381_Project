from Merged.Middleware.Strategy.PublisherStrategy import PublisherStrategy


class PublisherProxyStrategy(PublisherStrategy):
    def register(self, topics: list[str]):
        pass

    def publish(self, topic: str, value: str) -> None:
        pass
