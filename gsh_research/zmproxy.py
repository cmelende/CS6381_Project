import zmqmw as zmw

def main():
    broker = zmw.ProxyBroker()
    broker.start()

if __name__ == "__main__":
    main()