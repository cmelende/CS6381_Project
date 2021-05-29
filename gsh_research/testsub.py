import logging
import argparse
import zmqmw as zmw
import time
from uuid import uuid4

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

def resp_printer(topic, body):
    print(f"topic:{topic}, body:{body}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="name of your topic.", default="", nargs='?')
    parser.add_argument("timeout", help="seconds before process timeout", nargs='?', default=10, type=int)
    parser.add_argument("host", help="publisher (host)", type=str, default="localhost", nargs='?')
    parser.add_argument("port", help="port", type=int, default=5263, nargs='?')
    args = parser.parse_args()

    sub = zmw.Subscriber(host=args.host, port=args.port)

    sub.register_notify(args.topic, resp_printer)
    sub.register_sub(args.topic)

    # sub.register_notify("sam", resp_printer)
    # sub.register_sub(args.topic)

    # time.sleep(3) 
    # print("subscribing to 'kathleen' (no callback)") 
    # sub.register_sub("kathleen")

    # time.sleep(3)
    # print("adding callback")
    # sub.register_notify("kathleen", resp_printer)

    # time.sleep(3) 
    # print("unregistering 'sam'")
    # sub.unregister_sub("sam")

    # sub.regster_notify("kathleen", lambda x,y: print('second', y, x))

    if args.timeout != 0:
        try:
            time.sleep(args.timeout)
            sub.stop()
        except KeyboardInterrupt:
            pass

