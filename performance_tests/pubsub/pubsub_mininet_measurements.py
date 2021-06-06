import os.path

from mininet.cli import CLI
from mininet.net import Mininet
from time import sleep
import datetime

net = Mininet()

broker = net.addHost('broker')
pub01 = net.addHost('pub01')
sub01 = net.addHost('sub01')
sub02 = net.addHost('sub02')
sub03 = net.addHost('sub02')
sub04 = net.addHost('sub02')

s1 = net.addSwitch('s1')
controller = net.addController('controller')
net.addLink(s1, broker)
net.addLink(s1, sub01)
net.addLink(s1, sub02)
net.addLink(s1, sub03)
net.addLink(s1, sub04)
net.addLink(s1, pub01)
net.start()
sleep(1)
d = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(d)
print("Starting subscribers...")
broker.cmd(f'export PYTHONPATH=/home/gsh/code/distributed-systems-6381/CS6381_Project; python basic_proxy_cmdline.py -ba {broker.IP()} &')
sub01.cmd(f'export PYTHONPATH=/home/gsh/code/distributed-systems-6381/CS6381_Project; python basic_subscriber_cmdline.py -d {d} -n sub01 -ba {broker.IP()} &')
sub02.cmd(f'export PYTHONPATH=/home/gsh/code/distributed-systems-6381/CS6381_Project; python basic_subscriber_cmdline.py -d {d} -n sub02 -ba {broker.IP()} &')
sub03.cmd(f'export PYTHONPATH=/home/gsh/code/distributed-systems-6381/CS6381_Project; python basic_subscriber_cmdline.py -d {d} -n sub03 -ba {broker.IP()} &')
sub04.cmd(f'export PYTHONPATH=/home/gsh/code/distributed-systems-6381/CS6381_Project; python basic_subscriber_cmdline.py -d {d} -n sub04 -ba {broker.IP()} &')

sleep(2)
print('Starting publisher...')
pub01.cmd(f'export PYTHONPATH=/home/gsh/code/distributed-systems-6381/CS6381_Project; python basic_publisher_cmdline.py -ba {broker.IP()}  &')

#CLI(net)
print("sleeping....")
for i in range(100):
    net.pingAll(5)
    sleep(1)

print("Done.")
net.stop()
