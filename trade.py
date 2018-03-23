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
    conn.close()
except:
    pass



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
def buy(symbol,amount):
    print(getdatetime()+'===开始执行买入任务...')
    exchange = login()
    orderdata = exchange.create_market_buy_order(symbol=symbol, amount=amount)
    time.sleep(5)
    if orderdata['info']['status'] != 'ok':
        exchange.cancel_order(orderdata['id'])
        print('订单取消')
        return 'False'
    orderinfo = exchange.fetch_order(symbol=symbol, id=orderdata['id'])
    if orderinfo['status'] != 'closed':
        exchange.cancel_order(orderdata['id'])
        print('订单取消')
        return 'False'
    sqldata = "INSERT INTO t_order (id,dt,symbol,side,amount,filled,process) VALUES ('" + str(
        orderinfo['id']) + "','" + str(orderinfo['datetime']) + "','" + str(orderinfo['symbol']) + "','" + str(
        orderinfo['side']) + "','" + str(orderinfo['amount']) + "','" + str(orderinfo['filled']) + "','False')"
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(sqldata)
    conn.commit()
    conn.close()
    print(getdatetime()+'===买入成功')
    return 'True'


def sell(symbol,percent):
    print(getdatetime()+'===开始执行卖出任务...')
    exchange = login()
    sqldata = "SELECT id,amount,filled  from t_order WHERE process='False' AND symbol='"+str(symbol)+"'"
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    sqlresult = c.execute(sqldata)
    conn.commit()
    sumfilled = 0.0
    sumamount = 0.0
    idlist = []
    for row in sqlresult:
        sumfilled += row[2]
        sumamount += row[1]
        idlist.append(row[0])
    print('总成本:' + str(sumamount))
    print('总数量:' + str(sumfilled))
    print('关联单:' + str(idlist))
    wantprofit = (percent / 100) + 1 * sumamount
    orderbook = exchange.fetch_order_book(symbol=symbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    averageprice = (ask + bid) / 2
    profit = averageprice * sumfilled
    print('当前均价:' + str(averageprice)+',当前收益:'+str(profit)+',预期收益:' + str(wantprofit))
    if profit> wantprofit:
        orderdata = exchange.create_market_sell_order(symbol=symbol, amount=sumfilled)
        if orderdata['info']['status'] != 'ok':
            exchange.cancel_order(orderdata['id'])
            conn.close()
            print('订单取消')
            return 'False'
        orderinfo = exchange.fetch_order(symbol=symbol, id=orderdata['id'])
        if orderinfo['status'] != 'closed':
            exchange.cancel_order(orderdata['id'])
            conn.close()
            print('订单取消')
            return 'False'
        for oid in idlist:
            sqldata = "UPDATE t_order set process = 'True' WHERE id='" + str(oid) + "' AND symbol='"+str(symbol)+"'"
            c.execute(sqldata)
            conn.commit()
            conn.close()
        print('卖出成功')
        return 'True'
    conn.close()
    print(getdatetime()+'===未达卖出条件')
    return 'False'






    #   print(json.dumps(exchange.fetchOrders(symbol=SYMBOL, params={'status': 1}), indent=4))
