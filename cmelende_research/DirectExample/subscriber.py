from cmelende_research.DirectExample.MessageHandlers.TodaysWeatherMessageHandler import TodaysWeatherMessageHandler
from cmelende_research.N0mq.Broker.sub.Subscriber import Subscriber

host = "127.0.0.1"
pub_port = "5560"

if __name__ == '__main__':
    subscriber = Subscriber("WEATHER.TODAY")
    subscriber.set_handler(TodaysWeatherMessageHandler())
    subscriber.connect(host, pub_port)

    while True:
        try:
            subscriber.receive()
        except KeyboardInterrupt:
            print("closing...")
            subscriber.close()
