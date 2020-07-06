# coding=utf-8

from mininet.topo import Topo
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController

from datetime import datetime
import threading
import sys
import imp


nodes = []
mapping = {}
threads = []

hosts = []
switches = []

# 用来发包的host id
exp_hosts = [101, 118]
# 发包host与对应的指令字典
host_cmds = {
    'h101': 'tcpreplay --topspeed --intf1=eth0 test.pcap',
    'h106': '',
    'h114': '',
    'h118': 'tcpdump ' + '\'(src host 192.168.1.104 ) \' ' + '/tmppppp/cap.pcap '
}

def do_send_packet(host):
    print "send_packet"+host
    net.get_node(host).cmd(host_cmds[host])


def send_packet_timer(host):
    now_time = datetime.now()
    day_ = str(now_time.date().year) + '-' + str(now_time.date().month) + '-' + str(now_time.date().day)
    imp.acquire_lock()
    start_time = datetime.strptime(day_ + ' ' + sys.argv[1] + ':00', "%Y-%m-%d %H:%M:%S")
    imp.release_lock()
    timer_start_time = (start_time - now_time).total_seconds()
    print timer_start_time
    timer = threading.Timer(timer_start_time, do_send_packet, (host, ))
    timer.start()
    timer.join()


def add_sw(topo, n):
    for i in range(1, n + 1):
        topo.addSwitch('s' + str(i))
        switches.append('s' + str(i))


def add_host(topo, n, pos_start, pos_end):
    for i in range(pos_start, pos_end + 1):
        topo.addHost('h' + str(i), ip='192.168.' + str(n) + '.' + str(i), mac=Tools.makeMAC(i))
        hosts.append('h' + str(i))


def add_link_sw_host(topo, sw_num, host_start, host_end):
    for i in range(host_start, host_end + 1):
        topo.addLink('s' + str(sw_num), 'h' + str(i))


def add_link_sw_sw(topo, sw_num1, sw_num2):
    topo.addLink('s' + str(sw_num1), 's' + str(sw_num2))


def get_mappping():
    for node in nodes:
        mapping[node] = 0
    return mapping


def set_sw_worker(sw, worker):
    mapping[sw] = worker


class myTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(**opts)
        self.addHost()

def get_topo():
    topo = Topo()
    # 构造具体的拓扑
    # 192.168.1.x  x∈[101-105]
    # 192.168.2.x  x∈[106-113]
    # 192.168.3.x  x∈[114-117]
    # 192.168.4.x  x∈[118-121]
    add_sw(topo, 8)
    add_host(topo, 1, 101, 105)
    add_host(topo, 2, 106, 113)
    add_host(topo, 3, 114, 117)
    add_host(topo, 4, 118, 121)
    add_host(topo, 5, 122, 124)

    add_link_sw_host(topo, 1, 101, 105)
    add_link_sw_host(topo, 2, 106, 113)
    add_link_sw_host(topo, 3, 114, 117)
    add_link_sw_host(topo, 4, 118, 121)

    add_link_sw_host(topo, 5, 122, 122)
    add_link_sw_host(topo, 6, 123, 123)
    add_link_sw_host(topo, 7, 124, 124)

    add_link_sw_sw(topo, 8, 1)
    add_link_sw_sw(topo, 8, 2)
    add_link_sw_sw(topo, 8, 3)
    add_link_sw_sw(topo, 8, 4)
    add_link_sw_sw(topo, 8, 5)
    add_link_sw_sw(topo, 8, 6)
    add_link_sw_sw(topo, 8, 7)

    return topo

if __name__ == '__main__':
    topo = get_topo()

    net = Mininet(topo=topo, build=False)
    net.addController("controller", controller=RemoteController, ip="127.0.0.1", port=6633)
    net.start()
    print hosts

    for i in exp_hosts:
        t = threading.Thread(target=send_packet_timer, args=('h' + str(i),))
        threads.append(t)
        # t.setDaemon(False)
        t.start()

    for t in threads:
        t.join()

    exp.stop()
    print("all packet have been sent")



