import zmqmw as zmw
import logging
import argparse
import time

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    pub = zmw.NotifierBroker()
    pub.start()
