# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from currency import *

if __name__ == '__main__':

    scheduler = BlockingScheduler()

    scheduler.add_job(buycurrency, 'cron', second='59', minute=BUYMINUTE, hour='*/'+str(BUYHOUR), name='buytrade', id='buytrade')
    scheduler.add_job(sellcurrency, 'cron', second='0', minute=SELLMINUTE, hour=SELLHOUR, name='selltrade',
                      id='selltrade')
    scheduler.add_job(hardbuycurrency, 'cron', second='59', minute=HARDBUYMINUTE, hour='*/'+str(HARDBUYHOUR), name='hardbuytrade',
                      id='hardbuytrade')




    def increfreq(jobid, exechour, execminute):
        data = get_gbi_data()
        lendata = len(data)
        sumall = 0.0
        for s in data:
            sumall += s
        avg = sumall / lendata
        if data[-1] > 0 and avg > 0 and data[-1] < avg*0.9:
            job = scheduler.get_job(job_id=jobid)
            hour = None

            for f in job.trigger.fields:
                if f.name == 'hour':
                    hour = f
            if round(int(str(hour).split('/')[1])) != round(int(exechour)/2):
                hour = '*/'+str(round(int(exechour) / 2))
                job.reschedule(trigger='cron', second='59', minute=execminute, hour=hour)
                scheduler.print_jobs()
                log.warn('提高买入频率成功')
        return ''


    scheduler.add_job(increfreq, 'interval', hours=1, name='increfreq', id='increfreq',
                      args=['buytrade', BUYHOUR, BUYMINUTE])
    scheduler.add_job(increfreq, 'interval', hours=1, name='hardincrefreq', id='hardincrefreq',
                      args=['hardbuytrade', HARDBUYHOUR, HARDBUYMINUTE])

    log.warn('任务已启动')
    scheduler.print_jobs()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
