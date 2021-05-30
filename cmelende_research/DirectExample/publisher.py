from time import sleep

from cmelende_research.N0mq.Broker.pub.Publisher import Publisher

host = "127.0.0.1"
pub_port = "5560"

if __name__ == '__main__':
    publisher = Publisher()
    publisher.connect(host, pub_port, True)

    while True:
        try:
            sleep(5)
            publisher.publish("WEATHER", "NO RAIN THIS WEEK")
            publisher.publish("WEATHER.TODAY", "HIGH 99 LOW 60")
        except KeyboardInterrupt:
            publisher.close()
