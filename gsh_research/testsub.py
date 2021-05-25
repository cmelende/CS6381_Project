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
    args = parser.parse_args()

    sub = zmw.Subscriber()

    sub.notify("sam", resp_printer)
    sub.register_sub(args.topic)

    time.sleep(3) 
    print("subscribing to 'kathleen' (no callback)") 
    sub.register_sub("kathleen")

    time.sleep(3)
    print("adding callback")
    sub.notify("kathleen", resp_printer)

    time.sleep(3) 
    print("unregistering 'sam'")
    sub.unregister_sub("sam")

    sub.notify("kathleen", lambda x,y: print('second', y, x))

    if args.timeout != 0:
        try:
            time.sleep(args.timeout)
        except KeyboardInterrupt:
            pass
    sub.stop()

