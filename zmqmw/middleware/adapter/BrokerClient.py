from zmqmw.middleware.strategy.BrokerStrategy import BrokerStrategy


class BrokerClient:
    def __init__(self, broker_strategy: BrokerStrategy):
        """
        Creates a new broker client.

        :param broker_strategy: An object implementing a `BrokerStrategy`.
        """
        self._broker_strategy: BrokerStrategy = broker_strategy

    def run(self) -> None:
        self._broker_strategy.run()

    def close(self) -> None:
        self._broker_strategy.close()
