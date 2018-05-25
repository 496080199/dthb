# -*- coding: utf-8 -*-

import time, requests
from datetime import datetime, timedelta

headers = {
    'Host': 'api.feixiaohao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.feixiaohao.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

def datetime_to_timestamp(datetime_obj):
    """将本地(local) datetime 格式的时间 (含毫秒) 转为毫秒时间戳
    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
    :return: 13 位的毫秒时间戳  1456402864242
    """
    local_timestamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return local_timestamp




def get_gbi_data():
    now = datetime.now()
    last = now + timedelta(days=-300)
    r = requests.get('https://api.feixiaohao.com/gbi/' + str(datetime_to_timestamp(last)) + '/' + str(
        datetime_to_timestamp(now)) + '/',headers=headers).json()
    data = []
    for index, value in enumerate(r['gbi']):
        data.append(value[1])
    return data


def belowavg():
    data = get_gbi_data()
    lendata = len(data)
    sumall = 0.0
    for s in data:
        sumall += s
    avg = sumall / lendata
    if data[-1] > 0 and avg > 0 and data[-1] < avg:
        return True
    else:
        return False
def overavg():
    data = get_gbi_data()
    lendata = len(data)
    sumall = 0.0
    for s in data:
        sumall += s
    avg = sumall / lendata
    if data[-1] > 0 and avg > 0 and data[-1] > avg*1.15:
        return True
    else:
        return False

