# -*- coding: utf-8 -*-

import ccxt,time,json
import sqlite3

DB='huobipro.db'

conn = sqlite3.connect(DB)
c = conn.cursor()
try:
    c.execute('''CREATE TABLE t_order
      (id INT PRIMARY KEY     NOT NULL,
       dt   DATETIME   NOT NULL,
       symbol  CHAR(30)   NOT NULL,
       side    CHAR(10) NOT NULL,
       amount DECIMAL(20,20) NOT NULL,
       filled DECIMAL(20,20) NOT NULL,
       process  BOOLEAN NULL);''')
    conn.commit()
    conn.close()
except:
    pass



ACCKEY="451ea17c-77ed704a-f39aae0c-af477"
SECKEY="6204fb72-bde5858c-570def0b-deba4"
ACCOUNTID='781613'
SYMBOL='QTUM/USDT'


exchange = ccxt.huobipro()
exchange.apiKey = ACCKEY
exchange.secret = SECKEY

balance=exchange.fetch_balance()['info']['data']['list']

#for i in balance:
#    if i['currency'] == 'usdt' and i['type'] == 'trade':
 #       print('可用USDT:'+i['balance'])

def exesql(sqldata):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    cursor=c.execute(sqldata);
    conn.commit()
    conn.close()
    return cursor

def buy():
    orderdata=exchange.create_market_buy_order(symbol=SYMBOL, amount=0.1)
    time.sleep(10)
    if orderdata['info']['status'] != 'ok':
        exchange.cancel_order(orderdata['id'])
        return '订单取消'
    orderinfo=exchange.fetchOrder(symbol=SYMBOL,id=orderdata['id'])
    if orderinfo['status'] != 'close':
        exchange.cancel_order(orderdata['id'])
        return '订单取消'
    sqldata="INSERT INTO t_order (id,dt,symbol,side,amount,filled,process) VALUES " \
            "(int(orderinfo['id']),orderinfo['datetime'],orderinfo['symbol'],orderinfo['side']),orderinfo['amount'],orderinfo['filled'],FALSE)"

    exesql(sqldata)
    return '买入成功'

def sell():
    sqldata="SELECT id,amount,filled  from t_order WHERE process=FALSE "
    sqlresult=exesql(sqldata)
    sumfilled=0.0
    sumamount=0.0
    idlist=[]
    for row in sqlresult:
        sumfilled+=row[2]
        sumamount+=row[1]
        idlist.append(row[0])
    orderbook = exchange.fetch_order_book(symbol=SYMBOL)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    averageprice = (ask + bid)/2
    if averageprice*sumfilled >1.06*sumamount:
        orderdata = exchange.create_market_sell_order(symbol=SYMBOL, amount=sumfilled)
        if orderdata['info']['status'] != 'ok':
            exchange.cancel_order(orderdata['id'])
            return '订单取消'
        orderinfo = exchange.fetchOrder(symbol=SYMBOL, id=orderdata['id'])
        if orderinfo['status'] != 'close':
            exchange.cancel_order(orderdata['id'])
            return '订单取消'
        for oid in idlist:
            sqldata="UPDATE t_order set process = True WHERE ID="+str(oid)
        return '卖出成功'
    return '未达卖出条件'






    print(json.dumps(exchange.fetchOrders(symbol=SYMBOL, params={'status': 1}), indent=4))
