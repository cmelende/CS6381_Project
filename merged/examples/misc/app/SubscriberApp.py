from merged.examples.misc.app.App import App, TClient
from merged.examples.misc.app.options.SubscriberAppOptions import SubscriberAppOptions
from merged.examples.misc.value_objects.TopicHandlers import TopicHandler
from merged.implementations.notifier.subscriber.SubscriberNotifierStrategy import SubscriberNotifierStrategy
from merged.implementations.proxy.subscriber.SubscriberProxyStrategy import SubscriberProxyStrategy
from merged.middleware.adapter.SubscriberClient import SubscriberClient
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberApp(App):

    def __init__(self, app_options: SubscriberAppOptions):
        super().__init__(app_options)
        self.__subscriber_options = app_options

    def __create_client(self) -> TClient:
        strategy: SubscriberStrategy
        if self._use_proxy:
            strategy = SubscriberProxyStrategy(self.__subscriber_options.BrokerInfo,
                                               self.__subscriber_options.BrokerXPubPort,
                                               self.__subscriber_options.Logger,
                                               self.__subscriber_options.TopicHandlers)
        else:
            strategy = SubscriberNotifierStrategy(self.__subscriber_options.BrokerInfo,
                                                  self.__subscriber_options.Logger,
                                                  self.__subscriber_options.TopicHandlers)

        client: SubscriberClient = SubscriberClient(strategy)
        topic_handlers: TopicHandler
        for topic_handlers in self.__subscriber_options.TopicHandlers:
            client.subscribe(topic_handlers.Topic, topic_handlers.Handlers)

        return client

    def create_client(self) -> TClient:
        return self.__create_client()

