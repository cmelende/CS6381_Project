from N0mq.Broker.sub.SubscriberContainer import SubscriberContainer
from handlers.SportsMessageHandler import SportsMessageHandler
from handlers.SportsTopicHandler import StatsMessageHandler

host = "127.0.0.1"
broker_xpub_port = "5559"

if __name__ == '__main__':
    subscriberContainer = SubscriberContainer(host, broker_xpub_port)
    subscriberContainer.register_sub("SPORTS")
    subscriberContainer.register_sub("STATS")

    subscriberContainer.notify("SPORTS", SportsMessageHandler())
    subscriberContainer.notify("STATS", StatsMessageHandler())

    try:
        subscriberContainer.listen()
    except KeyboardInterrupt:
        print("Closing down")
        subscriberContainer.close()
