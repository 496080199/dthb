# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from currency import *



if __name__ == '__main__':



    scheduler = BlockingScheduler()
    scheduler.add_job(buycurrency, 'cron', second='59', minute=BUYMINUTE, hour=BUYHOUR,name='buytrade')
    scheduler.add_job(sellcurrency, 'cron', second='0', minute=SELLMINUTE, hour=SELLHOUR, name='selltrade')
    scheduler.add_job(hardbuycurrency, 'cron', second='59', minute=HARDBUYMINUTE, hour=HARDBUYHOUR, name='hardbuytrade')
    scheduler.add_job(hardsellcurrency, 'cron', second='0', minute=HARDSELLMINUTE, hour=HARDSELLHOUR, name='hardselltrade')
    log.warn('任务已启动')
    scheduler.print_jobs()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()