from mininet.cli import CLI
from mininet.net import Mininet
from time import sleep

net = Mininet()

broker = net.addHost('broker')
pub01 = net.addHost('pub01')
sub01 = net.addHost('sub01')
sub02 = net.addHost('sub02')

s1 = net.addSwitch('s1')
controller = net.addController('controller')
net.addLink(s1, broker)
net.addLink(s1, sub01)
net.addLink(s1, sub02)
net.addLink(s1, pub01)
net.start()

print('python notifier_broker.py 2>&1 >> broker.log &')
broker.cmd('python notifier_broker.py 2>&1 >> broker.log &')
print(f'python demo_publisher_with_notifier.py {broker.IP()} 5263 {pub01.IP()} 2>&1 >> pub01.log &')
pub01.cmd(f'python demo_publisher_with_notifier.py {broker.IP()} 5263 {pub01.IP()} 2>&1 >> pub01.log &')
print(f'python demo_subscriber_using_notifier.py {broker.IP()} 5263 sub01 {sub01.IP()} 2>&1 >> sub01.log &')
sub01.cmd(f'python demo_subscriber_using_notifier.py {broker.IP()} 5263 sub01 {sub01.IP()} 2>&1 >> sub01.log &')
sub02.cmd(f'python demo_subscriber_using_notifier.py {broker.IP()} 5263 sub01 {sub02.IP()} 2>&1 >> sub02.log &')
sleep(10)
net.stop()