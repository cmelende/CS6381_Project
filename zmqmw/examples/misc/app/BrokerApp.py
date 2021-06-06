from zmqmw.examples.misc.app.App import App, TClient
from zmqmw.examples.misc.app.options.BrokerAppOptions import BrokerAppOptions
from zmqmw.implementations.notifier.broker.BrokerNotifierStrategy import BrokerNotifierStrategy
from zmqmw.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy
from zmqmw.middleware.adapter.BrokerClient import BrokerClient
from zmqmw.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerApp(App):
    def __init__(self, app_options: BrokerAppOptions):
        super().__init__(app_options)
        self.__broker_app_options = app_options

    def create_client(self) -> TClient:
        strategy: BrokerStrategy
        if self._use_proxy:
            strategy = BrokerProxyStrategy(self.__broker_app_options.BrokerInfo.BrokerAddress,
                                           self.__broker_app_options.BrokerXSubPort,
                                           self.__broker_app_options.BrokerXPubPort,
                                           self.__broker_app_options.Logger)
        else:
            strategy = BrokerNotifierStrategy(self.__broker_app_options.BrokerInfo.BrokerAddress,
                                              self.__broker_app_options.BrokerInfo.BrokerPort,
                                              self.__broker_app_options.Logger)
        client = BrokerClient(strategy)

        return client