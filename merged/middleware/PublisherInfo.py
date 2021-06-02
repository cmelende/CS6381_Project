class PublisherInfo:
    def __init__(self, publisher_address: str, publisher_port_pool: list[str]):
        self.PublisherPortPool = publisher_port_pool
        self.PublisherAddress = publisher_address
