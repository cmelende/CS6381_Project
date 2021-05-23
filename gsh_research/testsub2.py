import logging
import argparse
import zmqmw as zmw
import time

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

def resp_printer(s):
    topic, body = str(s, encoding='utf-8').split(":")
    print(f"topic:{topic}, body:{body}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="name of your topic.", default="", nargs='?')
    parser.add_argument("timeout", help="seconds before process timeout", nargs='?', default=10, type=int)
    args = parser.parse_args()

    sub = zmw.Subscriber()
    sub.register_sub(args.topic, resp_printer)

    #sub.register_sub("kathleen")
    #sub.unregister_sub("sam")

    if args.timeout != 0:
        try:
            time.sleep(args.timeout)
        except KeyboardInterrupt:
            pass
    sub.stop()
