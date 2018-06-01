# -*- coding: utf-8 -*-

from decimal import Decimal
from common import *
from log import log

def buy(symbol,amount,table):
    log.warn(getdatetime()+'=='+str(symbol)+'==开始执行买入任务...')
    exchange = login()
    exchange.options['createMarketBuyOrderRequiresPrice'] = False
    orderdata = exchange.create_market_buy_order(symbol=symbol, amount=amount)
    time.sleep(5)
    if orderdata['info']['status'] != 'ok':
        exchange.cancel_order(orderdata['id'])
        log.warn('订单取消')
        return 'False'
    orderinfo = exchange.fetch_order(symbol=symbol, id=orderdata['id'])
    if orderinfo['status'] != 'closed':
        exchange.cancel_order(orderdata['id'])
        log.warn('订单取消')
        return 'False'
    filledamount = float(orderinfo['info']['field-amount']) - float(orderinfo['info']['field-fees'])
    sqldata = "INSERT INTO "+str(table)+" (id,dt,symbol,side,amount,filled,process) VALUES ('" + str(
        orderinfo['id']) + "','" + str(orderinfo['datetime']) + "','" + str(orderinfo['symbol']) + "','" + str(
        orderinfo['side']) + "','" + str(orderinfo['amount']) + "','" + str(filledamount) + "','0')"
    conn = opensqlconn()
    c = conn.cursor()
    c.execute(sqldata)
    conn.commit()
    conn.close()
    log.warn(getdatetime() +'=='+str(symbol)+'==买入成功')
    try:
        del exchange
    except:
        pass
    return 'True'


def sell(symbol,percent,table):
    log.warn(getdatetime()+'=='+str(symbol)+'==开始执行卖出任务...')
    exchange = login()
    sqldata = "SELECT id,amount,filled  from "+str(table)+" WHERE process='0' AND symbol='"+str(symbol)+"'"
    conn = opensqlconn()
    c = conn.cursor()
    c.execute(sqldata)
    sqlresult = c.fetchall()
    conn.commit()
    sumfilled = Decimal(0.0)
    sumamount = Decimal(0.0)
    idlist = []
    for row in sqlresult:
        sumfilled += row[2]
        sumamount += row[1]
        idlist.append(row[0])
    log.warn('总成本:' + str(sumamount))
    log.warn('总数量:' + str(sumfilled))
    log.warn('关联单:' + str(len(idlist)))
    wantprofit = ((Decimal(percent) / 100) + 1) * sumamount
    orderbook = exchange.fetch_order_book(symbol=symbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    averageprice = Decimal((ask + bid) / 2)
    sumfilled = sumfilled * Decimal(0.98)
    profit = averageprice * sumfilled
    if sumfilled == Decimal(0):
        profitprice=Decimal(0)
    else:
        profitprice = wantprofit / sumfilled
    log.warn('当前均价:' + str(averageprice) + ',卖出数量:' + str(sumfilled) + ',当前收益:' + str(profit) + ',预期收益:' + str(wantprofit) + ',预期均价:' + str(profitprice))
    if profit > wantprofit:
        try:
            exchange.create_market_sell_order(symbol=symbol, amount=sumfilled)
        except:
            log.warn('订单异常')
            return 'False'
        for oid in idlist:
            sqldata = "UPDATE "+str(table)+" set process = '1' WHERE id='" + str(oid) + "' AND symbol='"+str(symbol)+"'"
            c.execute(sqldata)
            conn.commit()
            log.warn('已更新订单' + str(oid) + '的状态')
        conn.close()
        log.warn(getdatetime() +'=='+str(symbol)+ '==卖出成功')
        return 'True'
    conn.close()
    log.warn(getdatetime() +'=='+str(symbol)+'==未达卖出条件')
    try:
        del exchange
    except:
        pass
    return 'False'

if __name__ == '__main__':
    sell(QTUMSYMBOL, QTUMPERCENT, QTUMTABLE)






    #   log.warn(json.dumps(exchange.fetchOrders(symbol=SYMBOL, params={'status': 1}), indent=4))
