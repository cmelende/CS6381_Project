class BrokerInfo:
    def __init__(self, broker_address: str, broker_pub_port: int = None, broker_sub_port: int = None):
        """
        Object to hold information about a `Broker`. Note, if the broker is in Notifier mode, the
        subscriber port may be omitted.

        :param broker_address: Address at which the broker is listening.
        :param broker_pub_port: The broker's publisher port.
        :param broker_sub_port: The broker's subscriber port.
        """
        self.BrokerPubPort = broker_pub_port
        self.BrokerSubPort = broker_sub_port
        self.BrokerAddress = broker_address
