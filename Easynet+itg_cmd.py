# # coding=utf-8
# from mininet.topo import Topo
# from mininet.net import Mininet
# from mininet.node import RemoteController
# from mininet.cli import CLI
# from mininet.link import TCLink
#
# from datetime import datetime
# import time
# import threading
# import random
# import sys
# import imp
#
# threads = []
# threads_receivers = []
# tcp_start_time = 20
# ITGSend_timer_start_time = 10  # 最晚的发送时间(单位：s)
# ITGSend_time_earliest = 0.5 * ITGSend_timer_start_time  # 最早发送时间
#
# cmd = 'ITGSend script_file'
# controller_ip = "10.15.123.112"  # 服务器的IP 10.15.123.112
#
# #  发包的线程，指定定时器
# def DITG_send_packet_timer(net, host):
#
#     threading_start = random.uniform(ITGSend_time_earliest, ITGSend_timer_start_time)
#     timer = threading.Timer(threading_start, do_DITG_send, (net, host, ))
#     timer.start()
#     timer.join()
#
#
# # 执行发包指令
# def do_DITG_send(net, host):
#     print time.time()
#     print net[host].cmd('ITGSend DITG_script_file/script_file_'+i) # todo 写script 按照script里面的进行发送
#
#
# # 收包的线程
# def DITG_recv_packet(net, host):
#     print(host + "receive begins")
#     net[host].cmd("ITGRecv &")
#
#
# # todo 确定收发主机
# senders = []
# receivers = []
#
#
# def add_sw(topo, n):
#     for i in range(1, n + 1):
#         topo.addSwitch('s' + str(i))
#
#
# def add_host(topo, n, **args):
#     # 因为主机可能需要指定MAC、IP这些属性，相对来说这个不是很好复用
#     for i in range(1, n + 1):
#         topo.addHost('h'+str(i), **args)
#
#
# def extract_switches(file):
#     file = open(unicode(file, 'utf-8'), "r")
#     switches = []
#     links = []
#     for line in file:
#         # find switch
#         if line.startswith("    id "):
#             token = line.split("\n")
#             token = token[0].split(" ")
#             line = line[7:]
#             if not line.startswith("\""):
#                 token = line.split("\n")
#                 switches.append(int(token[0])+1)
#         # find link 从1开始计数
#         if line.startswith("    source"):
#             token = line.split("\n")
#             token = token[0].split(" ")
#             sw1 = int(token[-1])+1
#         if line.startswith("    target"):
#             token = line.split("\n")
#             token = token[0].split(" ")
#             sw2 = int(token[-1])+1
#             links.append((sw1, sw2))
#
#     for s in switches:
#         pass
#         # self.addLink("h%s" %s, "s%s" %s, 0)
#
#     for dpid1, dpid2 in links:
#         pass
#         # self.addLink(node1="s%s" % dpid1, node2="s%s" % dpid2)
#     return links, switches
#
# # 100mbps的topo
# class simpleTopo(Topo):
#     def __init__(self, **opts):
#         Topo.__init__(self, **opts)
#         # links, switches = extract_switches("Easynet.gml")
#         # 直接提取link和switches了，不再从文件里面获取了
#
#         #  在原来的基础上进行了修改
#         #  1. 去掉了重复的node到node的线
#         #  2. 断掉了8和10的连接，让它8和10不会走一条link
#         link_modified = [(1, 2), (1, 4), (1, 8), (2, 7), (2, 8), (3, 4),
#                          (4, 8), (5, 6), (6, 9), (6, 11), (6, 14),
#                          (8, 18),  (10, 11), (10, 16), (10, 18), (11, 12), (11, 14),
#                          (11, 15), (12, 13), (12, 16), (13, 14), (14, 15), (15, 16),
#                          (17, 18), (18, 19)]
#         switch_num = 19
#         switches_extracted = [switch for switch in range(1, switch_num+1)]
#
#         # 先把本来图里需要添加的（交换机和交换机之间的线）加完
#         add_sw(self, switch_num)
#         add_host(self, switch_num)  # todo 分配主机数量
#
#         for dpid1, dpid2 in link_modified:
#
#             if dpid1 == 17 and dpid2 == 18:
#                 # 17-18上面
#                 bw = 1000  # 避免17-18的链路拥塞
#             else:
#                 bw = 50  # 其余带宽都是50bmps
#             self.addLink("s%s" % (int(dpid1)), "s%s" % (int(dpid2)), bw=bw)
#
#         # todo 修改收发主机的位置 主机分别分配一台直连的sw
#         for s in range(1, switch_num):
#             self.addLink("h%s" % s, "s%s" % s)
#
#
# if __name__ == '__main__':
#     print("main")
#     sim_topo = simpleTopo()
#     net = Mininet(topo=sim_topo, controller=None, build=False, link=TCLink)
#
#     controller = RemoteController("pox", ip=controller_ip, port=6633)
#     net.addController(controller)
#     net.start()
#
#     print("----- net topo setup ----- ")
#
#     # 接受方不需要同步，但是线程开起来以后就没有办法
#     for i in receivers:
#         t = threading.Thread(target=DITG_recv_packet, args=(net, i))
#         threads_receivers.append(t)
#         t.start()  # 因为是后台开着的，所以这里如果.join会导致主线程无法继续进行
#
#     print("----- receivers setup ----- ")
#
#     for i in senders:
#         t = threading.Thread(target=DITG_send_packet_timer, args=(net, i, ))
#         threads.append(t)
#         # t.setDaemon(False)
#         t.start()
#
#     for t in threads:
#         t.join()
#
#     CLI(net)
#
#     net.stop()
if __name__ == '__main__':
    print([i for i in range(1, 16+1)])
    print([i for i in range(17, 20+1)])
