## Assignment 1 Research Work - GSH

### The API
The middleware is wrapped into a package called `zmqmw` (for zmq middleware). There are a number of examples to demonstrate how the middleware can be used here.


### For Assignment 1 Requirements:

#### Task 1
Summary: `the publisherdirectly send the data to the subscribers who are interested in the topic`.

The design of the api works like this:
1. A broker exists that solely allows for the registration and listing of publishers - like a phone book.
2. A publisher comes online and registers its IP and port, along with a list of topics it may provide.
3. A subscriber comes online, queries this directory and then directly subscribes to topics for which it has an interest.

Running a demo:

1. Start the `notifier_broker.py`. This will come online and await publishers to register themselves.
2. Start the `demo_publisher_with_notifier.py` file to register the 'test_topic' and spin up a publisher on port 7777.
3. Start the `demo_subscriber_using_notifier.py` file to begin consuming the notifications.

#### Task 2
Summary: `publisheralways send the information to the broker, which then sends it to the subscribers`.

1. Start the `proxy_broker.py`. This will start a ProxyBroker on the default ports. This will show a message like:

```
gsh@fedora gsh_research]$ python3 proxy_broker.py 
INFO:distsys:initializing subscriber
INFO:distsys:initializing publisher.
INFO:distsys:	Proxy Broker Started...
INFO:distsys:	Listening for publisher on port: 5263
INFO:distsys:	Listening for subscribers on port: 5262
```

2. Start the `demo_pub_with_broker.py` (or multiple)

```
[gsh@fedora gsh_research]$ python3 demo_pub_with_broker.py
usage: demo_pub_with_broker.py [-h] topic count sleep
demo_pub_with_broker.py: error: the following arguments are required: topic, count, sleep
[gsh@fedora gsh_research]$ 
[gsh@fedora gsh_research]$ 
[gsh@fedora gsh_research]$ python3 demo_pub_with_broker.py test_topic 1000 250
INFO:distsys:Publisher sending to broker localhost:5263
INFO:distsys:Topic test_topic registered.
```

3. Start the `demo_subcriber.py` file with appropriate parameters

```
[gsh@fedora gsh_research]$ python3 demo_subscriber.py test_topic 10 localhost 5262
INFO:distsys:In TestSubscriber init
INFO:distsys:register_sub: topic: 'test_topic'
topic:test_topic, body:['1622335696.070675']
topic:test_topic, body:['1622335696.3211215']
topic:test_topic, body:['1622335696.5714617']
topic:test_topic, body:['1622335696.8218']
topic:test_topic, body:['1622335697.072138']
^Ctopic:test_topic, body:['1622335697.3224752']
topic:test_topic, body:['1622335697.5728154']
```

NOTE: if there are multiple subscribers code will need to be adjusted to subscribe to all of their topics or a blank topic subscribes to all.

## Technical Details
The API tries to abstract as much away from the user as possible. For example the proxy_broker and notifier_broker have only two lines of code each:

```
# proxy_broker.py
import zmqmw as zmw

def main():
    broker = zmw.ProxyBroker()
    broker.start()

if __name__ == "__main__":
    main()
```

Similarly, the complicated of the user-facing code is very straightforward to read. 

```
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
```

In the above each line of code should, to some degree, intuitively make sense.

Much more error handling should be added, though. The expectations of the library are not handled well if not met.