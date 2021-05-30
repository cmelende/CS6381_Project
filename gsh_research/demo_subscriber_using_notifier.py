import zmqmw as zmw
import json

def resp_printer(topic, body):
    print(f"topic:{topic}, body:{body}")

if __name__ == "__main__":

    broker = zmw.Broker('localhost', 5263, zmw.Broker.BrokerType.notifier)
    topics: dict = json.loads(zmw.Subscriber.get_publishers(broker=broker))

    subscribers = []

    for k, v in topics.items():
        s = zmw.Subscriber(host=v['ip'], port=v['port'])
        for t in v['topics']:
            s.register_notify(t, resp_printer)
            s.register_sub(t)
        subscribers.append(s)
    
