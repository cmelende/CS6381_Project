# CS6381_Project
###### Authors: Cory &amp; Sam's CS6381 Project

## NOTE TO GRADERS
Please see [GRADERS.md](https://github.com/cmelende/CS6381_Project/blob/main/GRADERS.md) for helpful notes.
## Documentation

This repository contains middleware built on top of 0MQ's pyzmq library. The middleware's aim is to provide a unified API for two different types of brokers in a pub/sub architecture. Namely:
- A broker acting as aproxy
- A broker acting as `notifier` whereby Publishers can register and Subscribers can get a list of publishers to whom they could subscribe directly.

### Terms and Definitions

* Message: These are considered the 'payload' for communication between Publishers and Subscribers, in the real world, these can either be bytes, strings, or (serialized) json objects that are later deserialized into in-memory objects.
* Topic: Strings that are assigned to each message that tells the Publisher or Subscriber what type of message it is. For Publishers, they are important in order to let the middleware know what types of messages they publish. For Subscribers, these are important to notify the middleware which messages they should receive.
* Subscriber: These are the receivers in the pub/sub architecture, they receive messages from Publishers directly or indirectly from a broker. Subscribers will only receive messages directly from publishers if you choose to run the middleware in the Notifier Mode, otherwise, Subscribers will receive messages from the broker in Proxy Mode.
* Publisher: These are the entities that send messages in the publisher/subscriber architecture, in our middleware they send messages either directly or indirectly to Subscribers, depending on if you are using Notifier Mode or Proxy Mode, respectively.  
* Broker: This middleware has two implementations of a broker, a broker that can run in Notifier Mode and a broker that can run in Proxy Mode. We will explain the differences later in this document but for now know that the broker in either mode assists in routing published messages from Publishers to Subscribers that are subscribed to those topics.
* Client: This is just a term for any application code that either utilizes the Publisher or Subscriber middleware of this project. The application code will handle the sending and receiving of messages through an abstraction (see 'Implementation Details' for info) without necessarily having to know about which implementation of the broker is being used.
* Mode: Refers to which implementation, Proxy or Notifier, is being used. There is a command line argument.

##### Notifier Mode
In the `Notifier Mode`, the Broker listens for Publisher's to register metadata about themselves (ip address, port, topics). When a Subscriber requests a list of publishers, the broker returns those data. With this data in-hand, a subscriber can directly contact the Publisher and subscribe.

##### Proxy Mode
In this mode, a `Publisher` publishes messages through the broker and a `Subscriber` subscribes through the broker. In this way, both Subscriber and Publisher remain anonymous to each other and the broker is handles proxying the data between interested parties.

#### API & Usages
We'll now go over how to interact with this system. The middleware is designed to be used by three different types of programs: 
* A broker program that should not need any application code beside what is provided by our middleware
* A subscriber program that can have additional application code besides what our middleware provides
* A publisher program that can also have additional application code besides what our middleware provides

##### Creating Clients
The client is the main class in our API with which you will interact. Basic examples can be found in the `testing_api` directory to get a sense of quickly utilizing the library and more sophisticated examples in the `zmqmw/examples` directory.

The middleware can be thought of being broken up into two different implementations, which dictates how the system's participants will interact with each other and must be used together in order for the system to work as intended:
* Notifier: BrokerNotifierStrategy, SubscriberNotifierStrategy, & PublisherNotifierStrategy -  this facilitates communication between subscribers and publishers directly.
* Proxy: BrokerProxyStrategy, SubscriberProxyStrategy, & PublisherProxyStrategy -  this facilitates communication between subscribers and publishers be decoupled, where messages are routed purely through a broker

An example of creating a Client may look like the following code snippet.
```
# notify the code where our broker lives...
broker = BrokerInfo(broker_address="127.0.0.1", broker_sub_port=6000)

pub_info = PublisherInfo(publisher_address='127.0.0.1', publisher_port=7000)

# select the strategy under which our broker is running (e.g. proxy or notifier)
strategy = PublisherNotifierStrategy(broker_info=broker, publisher_info=pub_info, logger=LocalLogger())

# create a publisher for the broker...
publisher = PublisherClient(strategy=strategy)
```

### BrokerClient
To create a broker client, all that is needed is to instantiate either a BrokerNotifierStrategy or a BrokerProxyStrategy and pass it into the BrokerClient. 

An example of creating a BrokerClient acting as a Proxy can be seen in the following snippet.
The parameters are:
- broker_address: address of the broker (localhost default)
- broker_xpub_port: the port which subscribers should hit
- broker_xsup_port: the port which publishers should hit
- logger: an optional parameter that takes in a Logger object (subclassed from `zmqmw.base_classes`) for your problem-dependent logging needs.
```
broker = BrokerProxyStrategy(broker_address="127.0.0.1",
                             broker_xpub_port=6000,
                             broker_xsub_port=7000,
                             logger=PrintLogger())
proxy = BrokerClient(broker)
```
Similarly, a BrokerClient in Notifier mode could easily be set-up as demonstrated below.
The parameters are:
- broker_address: address of the broker (localhost default)
- broker_port: The port listening for messages (from both Subscribers and Receivers)
- logger: an optional parameter that takes in a Logger object (subclassed from `zmqmw.base_classes`) for your problem-dependent logging needs.
```
broker = BrokerNotifierStrategy(broker_address="127.0.0.1",
                                broker_port=6000,
                                logger=PrintLogger())

proxy = BrokerClient(broker)
```

### PublisherClient
To create a publisher client, all that is needed is to instantiate either a PublisherNotifierStrategy or a PublisherProxyStrategy and pass it into the PublisherClient.

#### Proxy Mode:

```
# notify the code where our broker lives...
broker = BrokerInfo(broker_address="127.0.0.1", broker_sub_port=7000)

# select the strategy under which our broker is running (e.g. proxy or notifier)
strategy = PublisherProxyStrategy(broker_info=broker, logger=LocalLogger())

# create a publisher for the broker...
publisher = PublisherClient(strategy=strategy)
```
#### Notifier Mode:
```
# notify the code where our broker lives...
broker = BrokerInfo(broker_address="127.0.0.1", broker_sub_port=6000)

pub_info = PublisherInfo(publisher_address='127.0.0.1', publisher_port=7000)

# select the strategy under which our broker is running (e.g. proxy or notifier)
strategy = PublisherNotifierStrategy(broker_info=broker, publisher_info=pub_info, logger=LocalLogger())

# create a publisher for the broker...
publisher = PublisherClient(strategy=strategy)
```

### SubscriberClient

#### Proxy Mode:
```
# notify the code where our broker lives...
broker = BrokerInfo(broker_address="127.0.0.1", broker_pub_port=6000)

# select the strategy under which our broker is running (e.g. proxy or notifier)
strategy = SubscriberProxyStrategy(broker_info=broker, logger=LocalLogger())

# create a publisher for the broker...
subscriber = SubscriberClient(subscriber_strategy=strategy)

subscriber.subscribe(topic='timer', handlers=[TimerHandler()])
```
#### Notifier Mode:
```
broker = BrokerInfo(broker_address="127.0.0.1", broker_pub_port=6000)

# select the strategy under which our broker is running (e.g. proxy or notifier)
strategy = SubscriberNotifierStrategy(broker_info=broker, logger=LocalLogger())

# create a publisher for the broker...
subscriber = SubscriberClient(subscriber_strategy=strategy)
```

## Implementation Details
We will go over each part of the system. The main pattern we use in our middleware is the strategy pattern which you can read more [here](https://refactoring.guru/design-patterns/strategy/python/example).  We chose this pattern because as we expand the framework, the implementation details are abstracted from the user and can be interchanged relatively easily. You can see a UML diagram of how design in the following figure representing the `BrokerStrategy` object.

![broker patterns](./documentation/img/broker_patterns.jpg)

###### BrokerClient
This is a lightweight class that acts as the consumer of the BrokerStrategy abstract class, its main purpose is to delegate calls to run() & close() to a reference of BrokerStrategy, _brokerStrategy. As you can see, the BrokerClient is unaware of which BrokerStrategy implementation we use, it simply uses whichever Strategy that is passed in at runtime.

###### BrokerStrategy
This is an abstraction that allows the BrokerClient to be unaware of how the Publishers & Subscribers communicate with each other. It defines the following methods:

* run() - used by each implementation to setup what is needed, for our implementations it sets up the appropriate sockets that it will use to communicate with the Subscribers & Publishers
* close() - used by each implementation to teardown any resources that they need to free up - 0MQ documentation recommends that when you stop an application that you close each socket, otherwise some undefined behaviour may occur.
 
###### BrokerProxyStrategy
When this implementation is instantiated, we setup XPUB & XSUB sockets and setup a zmq.Proxy object, this object is what does the heavy lifting when Subsribers subscribe to topics and when Publishers publish to those topics. Below are descriptions of its methods:
* run() - starts up the zmq.proxy, which also starts to listen for any published messages
* close() - closes the XPUB & XSUB sockets and closes the 0MQ context

###### BrokerNotifierStrategy
When this implementation is instantiated, we setup a REP socket that handles two types of requests from either a Publisher or Subscriber
* `request\${topic}` - when the BrokerNotifierStrategy receives a REQ message with a payload starting with 'request$', which should be from a Subscriber, it parses the topic out of the payload and then returns all publishers of that topic. This allows any Subscribers using our middleware to Subscribe to a topic at any time and receive the most up to date Publishers that are publishing those topics. The subscriber can then connect to those publishers.
* `register\${json}` - When the BrokerNotifierStrategy receives a REQ message with a payload starting with 'register$', which should be from a Publisher, it parses the json out of the payload and then uses the object it parsed to register and store the information in a list for later retreival when a Subscriber asks for available Publishers. The object is in the form:
	```
	{
		ip: str
		port: str
		topics: list[str]
	}
	```

###### Subscriber Patterns
As can be seen in the figure below, the SubscriberStrategy object implements the Strategy pattern similar to the BrokerStrategy.

![subscriber patterns](./documentation/img/subscriber_pattern.jpg)

###### Subscriber Client
This is also a lightweight class that acts as the consumer of the SubscriberStrategy abstract class, it delegates calls to subscribe() and unsubscribe() to a SubscriberStrategy reference , _subscriberStrategy. Like the BrokerClient - this class in unaware of which SubscriberStrategy implementation is being used.

###### SubscriberStrategy
This is the abstraction that allows the SubscriberClient to be unaware of how the Subscribers subscribe to topics. It defines the following methods:
* subscribe(topic: str, handlers: list[MessageHandler]) - used by each implementation to setup the appropriate sockets in order to receive published messages. It also takes in a list of MessageHandlers which can be thought of as callback functions that occur when a message of the specified topic is received. Multiple handlers can handle one topic
* unsubscribe(topic:str) - used by each implementation to unsubscribe to a specified topic.
* listen() - used by each implementation to start the listening of each subscriber for published messages
* close() - used by each implementation to close down any sockets or 0MQ contexts

###### SubscriberProxyStrategy
This implementation's methods do the following:
* subscribe(topic: str, handlers: list[MessageHandler]) - Creates a ProxySubscriber object which is a helper class that holds a reference to a 0MQ SUB socket and the topic being subscribed to. It then connects to this socket and adds the ProxySubscriber to a list of Subscribers so when we can call listen(), we will know which subscribers we need to listen for
* unsubscribe(topic: str) - goes through the list of ProxySubscribers we keep track of and removes the subscribers that have the matching topic from the list and closes the socket
* listen() - Goes through the list of ProxySubscribers and listens on their sockets for any messages asynchronously.
* close() - simply goes through the list of ProxySubscribers and closes their sockets to free them up

###### SubscriberNotifierStrategy
When this implementation is created, it creates a REQ socket so we can later make requests to the NotifierBroker, the methods do the following:
* subscribe(topic: str, handlers: list[MessageHandler]) - Makes a request through the REQ socket with a string starting with 'request' (which to recap, causes the BrokerNotifierStrategy to receive that request and return all Publishers of that topic). For each publisher received, it creates a helper class, NotifierSubscriber, which connects to the publishers using what it received from the BrokerNotifierStrategy, then adds it to a list of NotifierSubscribers so we can use them to listen for messages.
* unsubscribe(topic: str) - Goes through the list of NotifierSubscribers and removes and closes any NotifierSubscribers that have a matching topic of the pass in topic parameter.
* listen() - Goes through the list of NotifierSubscribers and asynchronously listens for messages for each one.
* close() - Goes through the list of NotifierSubscribers and closes their sockets.

###### MessageHandlers
This is a pretty simple abstract class that allows developers to define how they want each topic to be handled. Its meant to be nothing fancy and can be thought of as a callback function that receives message payloads. In the future if we wanted to, it'll allow for more complex behavior such as serialization/deserialization, or to combine the use of other event driven patterns such as CQRS. 


###### Subscriber Patterns
</br></br>
![Publisher patterns](./documentation/img/publisher_patterns.jpg)
</br></br>

###### PublisherClient
This, like the other client classes, is a leightweight class that acts as the consumer of the abstract class, PublisherStrategy. It delegates calls to register() & publish() to a PublisherStrategy reference, _publisherStrategy. Like the others, this class is unaware of which PublisherStrategy implementation is being used.

###### PublisherStrategy
This is the abstraction that allows the PublisherClient to be unaware of how Publishers publish each topic. It defines the following methods:
* register(topic: list[str]) - Used by our implementations to alert the broker of the Publisher's existence
* publish(topic: str, val: str) - Used by our implementations to publish messages to the specified topic

###### PublisherProxyStrategy
This implementation's methods do the following:
* register(topic: list[str]) - Creates a helper class object, ProxyPublisher, which contains a reference to a 0MQ PUB socket. It then connects to this socket and adds it to a list of publishes it maintains a reference to
* publish(topic: str, val: str) - For each Publisher in the list of Publishers it keeps a reference to, it will publish the val string as a message to any Publishers that have a topic of the one specified

###### PublisherNotifierStrategy
When this implementation is instantiated, it will create a REQ socket and maintain a reference for later use, the implementation's methods do the following:
* register(topic: list[str]) - First it grabs a port off of the port pool that is provided to the strategy. It then creates a helper class object, NotifierPublisher, which contains a reference to a 0MQ PUB socket. It then binds to this socket using a port off of the port pool and adds it to a list of Publishers that it maintains a reference to. After this, it will notify the broker of the Publisher's existence by sending request using the REQ socket it created and sending a string containing a json object with the Publisher's information (remember the broker will receive this request and add it to the list of Publishers it maintains). The json object takes the form of:
	```
	{
		ip: str,
		port: str,
		topics: list[str]
	}
	
* publish(topic: str, val: str) - For each publisher in the list of publisher it keeps a reference to, it will publish the val string as a message to any Publishers that have a topic of the one specified.
###### Logger
This is an abstract class that we use to help us log various information (publishing, subscribing, registering). The default logger seen in `zmqmw.base_classes` does nothing. It can be subclassed, though, to accomplish whatever needs you may have.

## Closing Notes:
1. The security characteristics of this code have not been thoroughly vetted as it is a not a production-targeted project. As such, its is certainly highly exploitable and should not be used for anything other than learning purposes.
2. Due to the short time-frame of the class project, compounded with the scope of work, there are likely many bugs in the code. We'd love to hear about any that are found.
3. Some unit-tests require multiple-core CPUs because we start brokers, subscribers, and publishers in separate processes.


## Troubleshooting
1. If you cannot import the library, make sure the root directory of wherever `zmqmw` is in your PYTHONPATH environment variable. On unix-like operating systems this can usually be accomplished with the command `export PYTHONPATH=$PYTHONPATH:/folder/where/library/lives`.