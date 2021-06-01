from merged.examples.misc.app.App import App, TClient
from merged.examples.misc.app.options.AppOptions import AppOptions
from merged.implementations.notifier.BrokerNotifierStrategy import BrokerNotifierStrategy
from merged.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy
from merged.middleware.adapter.BrokerClient import BrokerClient
from merged.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerApp(App):
    def __init__(self, app_options: AppOptions):
        super().__init__(app_options)

    def create_client(self) -> TClient:
        strategy: BrokerStrategy
        if self._use_proxy:
            strategy = BrokerProxyStrategy()
        else:
            strategy = BrokerNotifierStrategy()
        client = BrokerClient(strategy)

        return client
