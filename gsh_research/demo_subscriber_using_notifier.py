import zmqmw as zmw
import json
import argparse
from time import time
from uuid import uuid4


hostname = None
localip = None
brokerip = None

def resp_printer(topic, body):
    f = float(body[0])
    n = float(time())
    with open(f"{brokerip}-{localip}.log", "a+") as file:
        msg = f"{brokerip},{localip},{f},{n},{n-f}"
        print(msg)
        file.write(msg + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("brokeraddress", help="IP Address of broker", default="localhost", nargs='?')
    parser.add_argument('brokerport', help="port of the broker", default="5263", type=int, nargs='?')
    parser.add_argument('name', help="name to record this host as", default=str(uuid4()), nargs='?')
    parser.add_argument('localip', help="local ip of this host", default="127.0.0.1", nargs='?')
    args = parser.parse_args()

    hostname = args.name
    localip = args.localip
    brokerip = args.brokeraddress

    broker = zmw.Broker(args.brokeraddress, args.brokerport, zmw.Broker.BrokerType.notifier)
    topics: dict = json.loads(zmw.Subscriber.get_publishers(broker=broker))

    subscribers = []

    for k, v in topics.items():
        s = zmw.Subscriber(host=v['ip'], port=v['port'])
        for t in v['topics']:
            s.register_notify(t, resp_printer)
            s.register_sub(t)
        subscribers.append(s)
 