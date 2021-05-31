import zmqmw as zmw
import json
import argparse
from time import time

def resp_printer(topic, body):
    #print(f"topic:{topic}, body:{body}")
    f = float(body[0])
    n = float(time())
    sender_timestamp = print(f"10.0.0.1,10.0.0.3,{f},{n},{n-f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("brokeraddress", help="IP Address of broker", default="localhost", nargs='?')
    parser.add_argument('brokerport', help="port of the broker", default="5263", type=int, nargs='?')
    args = parser.parse_args()

    broker = zmw.Broker(args.brokeraddress, args.brokerport, zmw.Broker.BrokerType.notifier)
    topics: dict = json.loads(zmw.Subscriber.get_publishers(broker=broker))

    print(json.dumps(topics,indent=4))

    subscribers = []

    for k, v in topics.items():
        s = zmw.Subscriber(host=v['ip'], port=v['port'])
        for t in v['topics']:
            s.register_notify(t, resp_printer)
            s.register_sub(t)
        subscribers.append(s)
 