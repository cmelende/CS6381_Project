from time import sleep

from cmelende_research.N0mq.Broker.pub.PublisherContainer import PublisherContainer

host = "127.0.0.1"
broker_xsub_port = "5560"

if __name__ == '__main__':
    publisherContainer = PublisherContainer(host, broker_xsub_port)
    publisherContainer.register_pub(["SPORTS"])
    publisherContainer.register_pub(["STATS"])

    should_continue = True
    while should_continue:
        try:
            sleep(5)
            publisherContainer.publish("SPORTS", "baseball")
            publisherContainer.publish("STATS", "Yankees: 1W-0L")
        except KeyboardInterrupt:
            print("Closing down")
            publisherContainer.close()
            should_continue = False
