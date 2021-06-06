from merged.middleware.adapter.BrokerClient import BrokerClient
from merged.implementations.proxy.BrokerProxyStrategy import BrokerProxyStrategy

broker = BrokerProxyStrategy("127.0.0.1", "5560", "5562")
proxy = BrokerClient(broker)

proxy.run()