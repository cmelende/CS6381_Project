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

sub_reads = 1000
pub_writes = 1000

d = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(d)

broker.cmd(f'python broker.py {broker.IP()} 5263 5262 proxy &')
sub01.cmd(f'python subscriber_one.py {broker.IP()} 5262 5263 {sub_reads} {d} sub01 proxy &')
sub02.cmd(f'python subscriber_one.py {broker.IP()} 5262 5263 {sub_reads} {d} sub02 proxy &')
sub03.cmd(f'python subscriber_one.py {broker.IP()} 5262 5263 {sub_reads} {d} sub03 proxy &')
#sub04.cmd(f'python subscriber_one.py {broker.IP()} 5262 5263 {sub_reads} {d} sub04 proxy &')
sleep(2)
pub01.cmd(f'python publisher_one.py {broker.IP()} 5263 {pub01.IP()} 7000 {pub_writes} proxy  &')
#CLI(net)
sleep(60)
net.stop()
