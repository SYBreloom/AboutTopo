# coding=utf-8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

from datetime import datetime
import time
import threading
import sys
import imp


senders = ['h1', 'h2', 'h3', 'h4']
receivers = ['h4', 'h5', 'h6', 'h7']
threads = []
threads_receivers = []
timer_start_time = 10  # send packet start in 10 seconds

cmd = 'ITGSend script_file'


# 执行发包指令
def do_DITG_send(net, host):
    print time.time()  # todo delete
    print net[host].cmd('ITGSend DITG_script_file/script_file_'+i)


#  发包的线程，指定定时器
def DITG_send_packet_timer(net, host):
    timer = threading.Timer(timer_start_time, do_DITG_send, (net, host, ))
    timer.start()
    timer.join()


# 收包的线程
def DITG_recv_packet(net, host):
    print(host + "receive begins")
    net[host].cmd("ITGRecv &")


# 一个很简单很简单的topo 用来flood对应的link
class simpleTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        self.addLink(s1, s2, bw=10)
        self.addLink(s2, s3, bw=10)

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        self.addLink(h1, s1, bw=10)
        self.addLink(h2, s1, bw=10)
        self.addLink(h3, s1, bw=10)

        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        self.addLink(h4, s2, bw=10)
        self.addLink(h5, s2, bw=10)

        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        self.addLink(s3, h6, bw=10)
        self.addLink(s3, h7, bw=10)

        '''
        #
        #       h2  h4
        #       |   |
        #   h1--s1--s2--s3--h7
        #       |   |   |
        #       h3  h5  h6
        #
        #
        #  h2 --> h5 h4
        #  h3 --> h4 h5
        #  h1 --> h7 h6
        #
        '''


if __name__ == '__main__':
    print("main")
    sim_topo = simpleTopo()
    net = Mininet(topo=sim_topo, controller=None, build=False, link=TCLink)

    controller = RemoteController("pox", ip="10.15.123.112", port=6633)
    net.addController(controller)
    net.start()

    print("----- net topo setup ----- ")

    # 接受方不需要同步，但是线程开起来以后就没有办法
    for i in receivers:
        t = threading.Thread(target=DITG_recv_packet, args=(net, i))
        threads_receivers.append(t)
        t.start()  # 因为是后台开着的，所以这里如果.join会导致主线程无法继续进行

    print("----- receivers setup ----- ")

    for i in senders:
        t = threading.Thread(target=DITG_send_packet_timer, args=(net, i, ))
        threads.append(t)
        # t.setDaemon(False)
        t.start()

    for t in threads:
        t.join()

    CLI(net)

    net.stop()
