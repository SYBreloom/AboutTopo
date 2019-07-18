# coding=utf-8

from datetime import datetime
import time
import threading
import sys


def printp(init_time):
    # print("tst")
    for i in range(init_time):
        print(init_time)


# 计算下一个1min以后的整点，返回需要的时间
def get_start_time():
    now_time = datetime.now()
    print "Enter time："+ time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    day_ = str(now_time.date().year) + '-' + str(now_time.date().month) + '-' + str(now_time.date().day)
    start_hour = now_time.hour
    start_min = now_time.minute+2
    if start_min >= 60:
        start_min = start_min - 60
        start_hour = start_hour+1

    start_time = datetime.strptime(day_ + " %s:%s:00"%(start_hour, start_min), "%Y-%m-%d %H:%M:%S")

    return (start_time-now_time).total_seconds(), start_time


if __name__ == "__main__":

    seconds, start_time = get_start_time()
    print(start_time)


