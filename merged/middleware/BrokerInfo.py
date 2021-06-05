class BrokerInfo:
    """
    Object to hold information about the broker.
    """
    def __init__(self, broker_address: str, broker_port: str):
        self.BrokerPort = broker_port
        self.BrokerAddress = broker_address
