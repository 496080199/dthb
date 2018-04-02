# -*- coding: utf-8 -*-

import ccxt, time,datetime ,json,pytz
import sqlite3
from config import *

tz = pytz.timezone('Asia/Shanghai')

conn = sqlite3.connect(DB)
c = conn.cursor()
try:
    c.execute('''CREATE TABLE t_order
      (id INT PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass

try:
    c.execute('''CREATE TABLE t_eos_order
      (id INT PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass

try:
    c.execute('''CREATE TABLE t_neo_order
      (id INT PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(40,30) NOT NULL,
       filled DECIMAL(40,30) NOT NULL,
       process  BOOLEAN NOT NULL);''')
    conn.commit()

except:
    pass
conn.close()



def login():
    exchange = ccxt.huobipro()
    exchange.apiKey = ACCKEY
    exchange.secret = SECKEY
    return exchange

    # balance=exchange.fetch_balance()['info']['data']['list']


# for i in balance:
#    if i['currency'] == 'usdt' and i['type'] == 'trade':
#       print('可用USDT:'+i['balance'])


def getdatetime():
    dt=datetime.datetime.now(tz).isoformat()
    return dt