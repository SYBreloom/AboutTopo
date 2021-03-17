# coding=utf-8

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import DefaultControllers
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

import sys


def get_topo():
    topo = Topo()

    # 构造具体的拓扑
    # 192.168.1.x  x∈[101-105]
    # 192.168.2.x  x∈[106-113]
    # 192.168.3.x  x∈[114-117]
    # 192.168.4.x  x∈[118-121]

    topo.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
    topo.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
    topo.addSwitch('s1')

    topo.addLink('s1', 'h1', cls=TCLink, bw=2)  # 不加TCLink 加不了bw关键字
    topo.addLink('s1', 'h2', cls=TCLink, bw=2)

    return topo


if __name__ == '__main__':
    setLogLevel("info")

    controller_ip = '127.0.0.1'

    if len(sys.argv) >= 2:
        controller_ip = str(sys.argv[1])
        controller = RemoteController('c', ip=controller_ip, port=6633)
        info("connect to remote controller, IP address %s \n" % controller_ip)
    else:
        controller = OVSController('c')
        info("start ovsController \n")

    topo = get_topo()
    net = Mininet(topo=topo, controller=None)

    net.addController(controller)
    net.start()


    CLI(net)

    net.stop()
