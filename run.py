# -*- coding: utf-8 -*-

from currency import *
from scheduler import *

if __name__ == '__main__':

    scheduler.add_job(buycurrency, 'cron', second='59', minute=BUYMINUTE, hour='*/' + str(BUYHOUR), name='buytrade',
                      id='buytrade')
    scheduler.add_job(sellcurrency, 'cron', second='30', minute=SELLMINUTE, hour=SELLHOUR, name='selltrade',
                      id='selltrade')
    scheduler.add_job(hardbuycurrency, 'cron', second='59', minute=HARDBUYMINUTE, hour='*/' + str(HARDBUYHOUR),
                      name='hardbuytrade',
                      id='hardbuytrade')

    scheduler.add_job(updategbi, 'cron', second='0', minute='*/30')

    scheduler.add_job(increfreq, 'cron', second='0', minute='50', name='increfreq', id='increfreq',
                      args=['buytrade', BUYHOUR, BUYMINUTE])
    scheduler.add_job(increfreq, 'cron', second='0', minute='51', name='hardincrefreq', id='hardincrefreq',
                      args=['hardbuytrade', HARDBUYHOUR, HARDBUYMINUTE])
    scheduler.add_job(backfreq, 'cron', second='0', minute='55', name='backfreq', id='backfreq',
                      args=['buytrade', BUYHOUR, BUYMINUTE])
    scheduler.add_job(backfreq, 'cron', second='0', minute='56', name='hardbackfreq', id='hardbackfreq',
                      args=['hardbuytrade', HARDBUYHOUR, HARDBUYMINUTE])

    log.warn('任务已启动')
    scheduler.print_jobs()
    printjobstolog()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
