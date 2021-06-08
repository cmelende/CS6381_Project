import os
from mininet.cli import CLI
from mininet.net import Mininet
from time import sleep
import datetime
import argparse


#####
# ENSURE CS6381_Project is in your PYTHONPATH!
####

def run_test(args):
    net = Mininet()
    sub_count = args.sub_count
    PYTHONPATH = args.pythonpath

    broker = net.addHost('broker')
    pub01 = net.addHost('pub01')
    s1 = net.addSwitch('s1')

    subs = []
    for i in range(sub_count):
        name = f"sub{i}"
        s = net.addHost(name)
        subs.append(s)
        net.addLink(s1, s)

    controller = net.addController('controller')
    net.addLink(s1, broker)
    net.addLink(s1, pub01)
    net.start()
    sleep(1)

    d = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(d)

    broker.cmd(f'export PYTHONPATH={PYTHONPATH}')
    pub01.cmd(f'export PYTHONPATH={PYTHONPATH}')
    broker.cmd(f'python basic_notifier_cmdline.py -ba {broker.IP()} &')
    sleep(2)
    pub01.cmd(f'python basic_publisher_notifier_cmdline.py -ba {broker.IP()} -pa {pub01.IP()} &')

    sleep(2)

    for s in subs:
        s.cmd(f'export PYTHONPATH={PYTHONPATH}')
        s.cmd(f'python basic_subscriber_notifier_cmdline.py -d {d} -n {s.name} -ba {broker.IP()} &')

    # CLI(net)
    print("sleeping....")
    for i in range(90):
        net.pingAll(10)
        sleep(5)

    print("Done.")
    net.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sub_count', help="Number of subscribers.", type=int, default=1)
    parser.add_argument('-p', '--pythonpath', help="Python path", type=str)
    args = parser.parse_args()
    run_test(args)
