import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

def work():
    print("TimeNow in func: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return

def scheduler(sched):
    # trigger = ``date``, ``interval`` or ``cron``
    sched.add_job(work, 'interval', seconds=3, id='my_job_id')

    print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    ## 会阻塞挂起当前线程
    sched.start()
    print("TimeNow end: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    exit()

def scheduler_cron(sched):

    # 每周一到周五运行 直到 2024-05-30 00:00:00
    sched.add_job(work, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2024-05-30')
    print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    ## 会阻塞挂起当前线程
    sched.start()


def test():
    sched = BackgroundScheduler()
    sched.add_job(work, 'interval', seconds=3)

    print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    sched.start()

    #不会阻塞主线程
    print("TimeNow end: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    while True:
        print("1111111")
        time.sleep(1)


if __name__ == '__main__':
    #sched = BlockingScheduler()
    #scheduler(sched)
    test()
