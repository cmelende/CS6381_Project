from merged.examples.misc.app.App import App, TClient
from merged.examples.misc.app.options.SubscriberAppOptions import SubscriberAppOptions
from merged.examples.misc.value_objects.TopicHandlers import TopicHandler
from merged.implementations.notifier.SubscriberNotifierStrategy import SubscriberNotifierStrategy
from merged.implementations.proxy.SubscriberProxyStrategy import SubscriberProxyStrategy
from merged.middleware.adapter.SubscriberClient import SubscriberClient
from merged.middleware.strategy.SubscriberStrategy import SubscriberStrategy


class SubscriberApp(App):
    def __init__(self, app_options: SubscriberAppOptions):
        super().__init__(app_options)
        self.__subscriber_options = app_options

    def run(self) -> TClient:
        strategy: SubscriberStrategy()
        if self._use_proxy:
            strategy = SubscriberProxyStrategy()
        else:
            strategy = SubscriberNotifierStrategy()

        client: SubscriberClient = SubscriberClient(strategy)
        topic_handlers: TopicHandler
        for topic_handlers in self.__subscriber_options.TopicHandlers:
            client.subscribe(topic_handlers.Topic, topic_handlers.Handlers)

        return client
