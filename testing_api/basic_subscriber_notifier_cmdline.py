import argparse
from zmqmw.implementations.notifier.subscriber.SubscriberNotifierStrategy import SubscriberNotifierStrategy
from zmqmw.middleware.BrokerInfo import BrokerInfo
from zmqmw.middleware.adapter.SubscriberClient import SubscriberClient

# we create an OPTIONAL logger, for demonstration purposes
from zmqmw.middleware.handler.MessageHandler import MessageHandler


# an OPTIONAL logger we can use for our strategy
class LocalLogger:
    def log(self, val: str):
        print(val)


# this is used on line 30 to show how we might handle an event...
class TimerHandler(MessageHandler):
    def handle_message(self, value: str) -> None:
        print(f"TimerHandler: {value}")


def main(args):
    # notify the code where our broker lives...
    broker = BrokerInfo(broker_address="127.0.0.1", broker_pub_port=6000)

    # select the strategy under which our broker is running (e.g. proxy or notifier)
    strategy = SubscriberNotifierStrategy(broker_info=broker, logger=LocalLogger())

    # create a publisher for the broker...
    subscriber = SubscriberClient(subscriber_strategy=strategy)

    subscriber.subscribe(topic='timer', handlers=[TimerHandler()])

    try:
        subscriber.listen()
    except KeyboardInterrupt:
        subscriber.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ba', "--broker_address", help="IP Address of broker", default="127.0.0.1", type=str,
                        nargs='?')
    parser.add_argument('-bp', '--broker_port', help="Broker info port", default=6000, type=int, nargs='?')
    args = parser.parse_args()
    main(args)
