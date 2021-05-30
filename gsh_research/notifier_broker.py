import zmqmw as zmw
import logging
import argparse
import time

logging.basicConfig()
log = logging.getLogger('distsys')
log.setLevel(logging.INFO)

if __name__ == "__main__":

    # this broker acts as a store for publishers to publish their locations
    # and for subscribers to acquire that information.
    pub = zmw.NotifierBroker(port=5263)
    pub.start()
