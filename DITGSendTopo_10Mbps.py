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



threads = []
threads_receivers = []
timer_start_time = 10  # send packet start in 10 seconds

cmd = 'ITGSend script_file'


#  发包的线程，指定定时器
def DITG_send_packet_timer(net, host):
    # todo 加一个random让它逐渐开始发送，而不是burst
    timer = threading.Timer(timer_start_time, do_DITG_send, (net, host, ))
    timer.start()
    timer.join()


# 执行发包指令
def do_DITG_send(net, host):
    print time.time()  # todo delete
    print net[host].cmd('ITGSend DITG_script_file/script_file_'+i) # 按照script里面的进行发送



# 收包的线程
def DITG_recv_packet(net, host):
    print(host + "receive begins")
    net[host].cmd("ITGRecv &")


senders = ['h1', 'h2', 'h3', 'h4']
receivers = ['h4', 'h5', 'h6', 'h7']
sw_list = ['s0', ]

def add_sw(topo, n):
    for i in range(1, n + 1):
        topo.addSwitch('s' + str(i))
        sw_list.append('s' + str(i))

# 10mbps的
class simpleTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        add_sw(self, 10)

        # s1
        h1 = self.addHost('h1')
        self.addLink('h1', 's1')

        # s2
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        self.addLink('h2', 's2')
        self.addLink('h3', 's2')

        # s3
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        self.addLink('h4', 's3')
        self.addLink('h5', 's3')
        self.addLink('h6', 's3')

        # s4
        h7 = self.addHost('h7')
        self.addLink('h7', 's4')

        self.addLink('s1', 's5')
        self.addLink('s2', 's5')
        self.addLink('s3', 's5')
        self.addLink('s4', 's5')
        self.addLink('s5', 's7')
        self.addLink('s5', 's6', bw=10, delay='2ms', loss=1, max_queue_size=1000)
        self.addLink('s6', 's8', bw=10)
        self.addLink('s6', 's9')
        self.addLink('s6', 's10')

        # Target server 1
        h8 = self.addHost('h8')
        self.addLink('h8', 's8')

        # decoy server 1
        h9 = self.addHost('h9')
        self.addLink('h8', 's9')

        # decoy server 2
        h10 = self.addHost('h10')
        self.addLink('h10', 's10')


if __name__ == '__main__':
    print("main")
    sim_topo = simpleTopo()
    net = Mininet(topo=sim_topo, controller=None, build=False, link=TCLink)

    controller = RemoteController("pox", ip="10.180.114.148", port=6633)
    net.addController(controller)
    net.start()

    print("----- net topo setup ----- ")


    # # 接受方不需要同步，但是线程开起来以后就没有办法
    # for i in receivers:
    #     t = threading.Thread(target=DITG_recv_packet, args=(net, i))
    #     threads_receivers.append(t)
    #     t.start()  # 因为是后台开着的，所以这里如果.join会导致主线程无法继续进行
    #
    # print("----- receivers setup ----- ")
    #
    # for i in senders:
    #     t = threading.Thread(target=DITG_send_packet_timer, args=(net, i, ))
    #     threads.append(t)
    #     # t.setDaemon(False)
    #     t.start()
    #
    # for t in threads:
    #     t.join()

    CLI(net)

    net.stop()
