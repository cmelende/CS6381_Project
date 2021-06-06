from zmqmw.examples.misc.app.App import App, TClient
from zmqmw.examples.misc.app.options.SubscriberAppOptions import SubscriberAppOptions
from zmqmw.examples.misc.value_objects.TopicHandlers import TopicHandler
from zmqmw.implementations.notifier.subscriber.SubscriberNotifierStrategy import SubscriberNotifierStrategy
from zmqmw.implementations.proxy.subscriber.SubscriberProxyStrategy import SubscriberProxyStrategy
from zmqmw.middleware.adapter.SubscriberClient import SubscriberClient
from zmqmw.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberApp(App):

    def __init__(self, app_options: SubscriberAppOptions):
        super().__init__(app_options)
        self.__subscriber_options = app_options

    def __create_client(self) -> TClient:
        strategy: SubscriberStrategy
        if self._use_proxy:
            strategy = SubscriberProxyStrategy(self.__subscriber_options.BrokerInfo,
                                               self.__subscriber_options.BrokerXPubPort,
                                               self.__subscriber_options.Logger)
        else:
            strategy = SubscriberNotifierStrategy(self.__subscriber_options.BrokerInfo,
                                                  self.__subscriber_options.Logger)

        client: SubscriberClient = SubscriberClient(strategy)
        topic_handlers: TopicHandler
        for topic_handlers in self.__subscriber_options.TopicHandlers:
            client.subscribe(topic_handlers.Topic, topic_handlers.Handlers)

        return client

    def create_client(self) -> TClient:
        return self.__create_client()

