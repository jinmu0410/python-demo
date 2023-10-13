
"""
调度的使用
"""
import time
import datetime
from threading import Timer
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

def print_hello():
    print("TimeNow in func: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def test1():
    # Threading中的timer,延迟两秒
    t = Timer(2, print_hello)
    print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    t.start()
    print("TimeNow end: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    exit()


def test2():
    scheduler = BlockingScheduler()
    scheduler.add_job(print_hello, trigger='interval', id = '123', minutes=1)
    print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    scheduler.start()
    print("TimeNow end: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    exit()


def test3():
    sched = BackgroundScheduler()
    sched.add_job(print_hello, 'interval', seconds=3)
    sched.start()

if __name__ == '__main__':
    #test1()
    #test2()
    test3()


