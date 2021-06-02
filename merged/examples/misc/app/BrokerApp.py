from merged.examples.misc.app.App import App, TClient
from merged.examples.misc.app.options.BrokerAppOptions import BrokerAppOptions
from merged.implementations.notifier.BrokerNotifierStrategy import BrokerNotifierStrategy
from merged.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy
from merged.middleware.adapter.BrokerClient import BrokerClient
from merged.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerApp(App):
    def __init__(self, app_options: BrokerAppOptions):
        super().__init__(app_options)
        self.__broker_app_options = app_options

    def create_client(self) -> TClient:
        strategy: BrokerStrategy
        if self._use_proxy:
            strategy = BrokerProxyStrategy(self.__broker_app_options.BrokerAddress,
                                           self.__broker_app_options.BrokerXSubPort,
                                           self.__broker_app_options.BrokerXPubPort)
        else:
            strategy = BrokerNotifierStrategy(self.__broker_app_options.BrokerXPubPort)
        client = BrokerClient(strategy)

        return client
