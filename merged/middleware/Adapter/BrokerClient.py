from merged.middleware.Strategy.BrokerStrategy import BrokerStrategy


class BrokerClient:
    def __init__(self, broker_strategy: BrokerStrategy):
        self._broker_strategy: BrokerStrategy = broker_strategy

    def run(self) -> None:
        self._broker_strategy.run()
