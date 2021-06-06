import os
from mininet.cli import CLI
from mininet.net import Mininet
from time import sleep
import datetime

#####
# ENSURE CS6381_Project is in your PYTHONPATH!
####

net = Mininet()

broker = net.addHost('broker')
pub01 = net.addHost('pub01')
sub01 = net.addHost('sub01')

s1 = net.addSwitch('s1')
controller = net.addController('controller')
net.addLink(s1, broker)
net.addLink(s1, sub01)
net.addLink(s1, pub01)
net.start()
sleep(1)

d = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(d)

broker.cmd(f'export PYTHONPATH={os.environ.get("PYTHONPATH")}')
pub01.cmd(f'export PYTHONPATH={os.environ.get("PYTHONPATH")}')
sleep(1)
sub01.cmd(f'export PYTHONPATH={os.environ.get("PYTHONPATH")}')
broker.cmd(f'python basic_notifier_cmdline.py -ba {broker.IP()} &')
pub01.cmd(f'python basic_publisher_notifier_cmdline.py -ba {broker.IP()} -pa {pub01.IP()} &')
sub01.cmd(f'python basic_subscriber_notifier_cmdline.py -d {d} -n sub01 -ba {broker.IP()}')

CLI(net)
print("sleeping....")
for i in range(100):
    net.pingAll(5)
    sleep(1)

print("Done.")
net.stop()
