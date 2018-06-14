# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from fxhgbi import *
from log import *
from common import *

scheduler = BlockingScheduler(timezone=tz)


def printjobstolog():
    sc = open('scheduler.log', 'a+')
    sc.write(str(getdatetime() + '\n'))
    scheduler.print_jobs(out=sc)
    sc.close()

def increfreq(jobid, exechour, execminute):
    davg, lastdata = getdavglastdata()
    if lastdata > 0 and davg > 0 and lastdata < davg * float(FREQ):
        job = scheduler.get_job(job_id=jobid)
        hour = None

        for f in job.trigger.fields:
            if f.name == 'hour':
                hour = f
        if round(int(str(hour).split('/')[1])) != round(int(exechour) / 2):
            hour = '*/' + str(round(int(exechour) / 2))
            job.reschedule(trigger='cron', second='59', minute=execminute, hour=hour)
            printjobstolog()
            log.warn('提高买入频率成功')
    return ''


def backfreq(jobid, exechour, execminute):
    davg, lastdata = getdavglastdata()
    if lastdata > 0 and davg > 0 and lastdata > davg * float(FREQ):
        job = scheduler.get_job(job_id=jobid)
        hour = None

        for f in job.trigger.fields:
            if f.name == 'hour':
                hour = f
        if round(int(str(hour).split('/')[1])) != round(int(exechour)):
            job.reschedule(trigger='cron', second='59', minute=execminute, hour='*/' + str(exechour))
            printjobstolog()
            log.warn('恢复买入频率成功')
    return ''


if __name__ == '__main__':
    pass

