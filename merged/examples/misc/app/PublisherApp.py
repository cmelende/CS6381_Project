from merged.examples.misc.app.App import App, TClient
from merged.examples.misc.app.options.PublisherAppOptions import PublisherAppOptions
from merged.implementations.notifier.PublisherNotifierStrategy import PublisherNotifierStrategy
from merged.implementations.proxy.publisher.PublisherProxyStrategy import PublisherProxyStrategy
from merged.middleware.adapter.PublisherClient import PublisherClient
from merged.middleware.strategy.PublisherStrategy import PublisherStrategy


class PublisherApp(App):
    def __init__(self, app_options: PublisherAppOptions):
        super().__init__(app_options)
        self.__publisher_app_options = app_options

    def create_client(self) -> TClient:
        strategy: PublisherStrategy
        if self._use_proxy:
            strategy = PublisherProxyStrategy(self.__publisher_app_options.BrokerInfo)
        else:
            strategy = PublisherNotifierStrategy(self.__publisher_app_options.BrokerInfo,
                                                 self.__publisher_app_options.PublisherInfo)

        client = PublisherClient(strategy)

        for pub_topics in self.__publisher_app_options.PublisherTopics:
            client.register(pub_topics.Topics)

        return client