# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from trade import *
import logging


if __name__ == '__main__':
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)


    scheduler = BlockingScheduler()
    scheduler.add_job(buy, 'cron', second='0', minute=buyminute, hour=buyhour,id='buy')
    scheduler.add_job(sell, 'cron', second='0', minute=sellminute, hour=sellhour,id='sell')
    print('任务已启动')
    print(str(scheduler.print_jobs()))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()