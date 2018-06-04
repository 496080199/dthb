# -*- coding: utf-8 -*-

import time, requests
from datetime import timedelta
from common import *



headers = {
    'Host': 'api.feixiaohao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.feixiaohao.com/gbi/',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

headers2 = {
    'Host': 'gbi.inblockchain.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://inblockchain.com/',
    'Origin': 'http://inblockchain.com',
    'DNT': '1',
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
    for i in range(3):
        try:
            now = datetime.datetime.now()
            last = now + timedelta(days=-300)
            r = requests.get('https://api.feixiaohao.com/gbi/' + str(datetime_to_timestamp(last)) + '/' + str(
                datetime_to_timestamp(now)) + '/',headers=headers).json()
            data = []
            for index, value in enumerate(r['gbi']):
                data.append(value[1])
            return data
        except:
            continue

def get_last_gbi_data():
    for i in range(3):
        try:
            gbidata = requests.get('http://gbi.inblockchain.com/markets/gbi?json=1',headers2).json()
            return gbidata['gbi']
        except:
            continue
    return None

def updategbi():
    data = get_gbi_data()
    lendata = len(data)
    sumall = 0.0
    for s in data:
        sumall += s
    davg = sumall / lendata
    lastdata=get_last_gbi_data()
    if lastdata is None:
        lastdata=data[-1]
    sqldata = "INSERT INTO t_gbi (dt,davg,lastdata) VALUES ('"+str(datetime.datetime.now())+"','"+str(davg)+"','"+str(lastdata)+"');"
    deletesqldata = "DELETE FROM t_gbi WHERE dt < '"+str(datetime.datetime.now() +timedelta(days=-7))+"';"
    conn = opensqlconn()
    c = conn.cursor()
    c.execute(sqldata)
    conn.commit()
    conn.close()
    conn = opensqlconn()
    c = conn.cursor()
    c.execute(deletesqldata)
    conn.commit()
    conn.close()
    return ''

def getdavglastdata():
    sqldata = "select davg,lastdata from t_gbi order by dt desc limit 1;"
    conn = opensqlconn()
    c = conn.cursor()
    c.execute(sqldata)
    sqlresult = c.fetchall()
    lastdata = 0.0
    davg = 0.0
    for row in sqlresult:
        davg = float(row[0])
        lastdata = float(row[1])
    return davg,lastdata

def belowavg():
    davg,lastdata=getdavglastdata()
    if lastdata > 0 and davg > 0 and lastdata < davg*0.95:
        return True
    else:
        return False
def overavg():
    davg, lastdata = getdavglastdata()
    if lastdata > 0 and davg > 0 and lastdata > davg*1.15:
        return True
    else:
        return False




if __name__ == '__main__':
    updategbi()


