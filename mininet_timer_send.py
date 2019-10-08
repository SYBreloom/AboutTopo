# coding=utf-8
import datetime
def timer_send():
    import os
    print(datetime.datetime.now().strftime('%H:%M:%S.%f'))
    os.system("tcpreplay --intf1=h123-eth0 --multiplier=0.7 -L 8000 0918pcap/core_attack_sum.pcap")
    

if __name__ == "__main__":

    import imp
    import threading
    now_time = datetime.datetime.now()


    # print "Enter time："+ time.strftime("%a %b %d %H:%M:%S", time.localtime())
    day_ = str(now_time.date().year) + '-' + str(now_time.date().month) + '-' + str(now_time.date().day)
    start_hour = now_time.hour
    start_min = now_time.minute + 1
	# 直接下一个整点
    if start_min >= 60:
        start_min = start_min - 60
        start_hour = start_hour + 1

    imp.acquire_lock()
    start_time = datetime.datetime.strptime(day_ + " %s:%s:00" % (start_hour, start_min), "%Y-%m-%d %H:%M:%S")
    imp.release_lock()
    wait_seconds = (start_time - now_time).total_seconds()

    timer = threading.Timer(wait_seconds, timer_send, ())
    timer.start()
    timer.join()
