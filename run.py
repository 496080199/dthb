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
    scheduler.add_job(buy, 'cron', second='30', minute=QTUMBUYMINUTE, hour=QTUMBUYHOUR,name='qtumbuy', kwargs={'symbol':QTUMSYMBOL,'amount':QTUMAMOUNT})
    scheduler.add_job(sell, 'cron', second='0', minute=QTUMSELLMINUTE, hour=QTUMSELLHOUR,name='qtumsell', kwargs={'symbol':QTUMSYMBOL,'percent':QTUMPERCENT})
    print('任务已启动')
    print(str(scheduler.print_jobs()))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()