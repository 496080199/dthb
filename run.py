# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from currency import *
import logging


if __name__ == '__main__':
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)


    scheduler = BlockingScheduler()
    scheduler.add_job(buycurrency, 'cron', second='59', minute=BUYMINUTE, hour=BUYHOUR,name='buytrade')
    scheduler.add_job(sellcurrency, 'cron', second='0', minute=SELLMINUTE, hour=SELLHOUR, name='selltrade')
    print('任务已启动')
    print(str(scheduler.print_jobs()))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()