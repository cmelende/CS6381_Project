from cmelende_research.N0mq.Broker.BrokerProxy import BrokerProxy

host = "127.0.0.1"
xpub_port = "5559"
xsub_port = "5560"

if __name__ == '__main__':
    brokerProxy = BrokerProxy(host, xsub_port, xpub_port)
    should_continue = True
    while should_continue:
        try:
            brokerProxy.run()
        except KeyboardInterrupt:
            print("Closing down")
            brokerProxy.close()
            should_continue = False
