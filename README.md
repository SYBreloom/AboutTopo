# AboutTopo

关于mininet下的拓扑和一些cmd的命令管理

##### simpletopo

一个比较简单的拓扑，仅仅设定了带宽bw，主机和链路数量有限

##### ddos_topo

之前师兄毕设的拓扑，有各个主机的多线程cmd，定时执行线程，定时方式为参数指定

##### DITGSend_topo

这是在simpletopo的基础上添加了多线程cmd，区分了receiver和sender的行为
其中receiver的行为放在了后台，sender的则是仿照了前面，以多线程的方式，配合DITG的脚本执行

##### DITGSendTopo_10Mbps

10Mbps的拓扑，用DITG产生流量
