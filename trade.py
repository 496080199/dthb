# -*- coding: utf-8 -*-

from common import *

def buy(symbol,amount,table):
    print(getdatetime()+'=='+str(symbol)+'==开始执行买入任务...')
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
    filledamount = float(orderinfo['info']['field-amount']) - float(orderinfo['info']['field-fees'])
    sqldata = "INSERT INTO "+str(table)+" (id,dt,symbol,side,amount,filled,process) VALUES ('" + str(
        orderinfo['id']) + "','" + str(orderinfo['datetime']) + "','" + str(orderinfo['symbol']) + "','" + str(
        orderinfo['side']) + "','" + str(orderinfo['amount']) + "','" + str(filledamount) + "','False')"
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(sqldata)
    conn.commit()
    conn.close()
    print(getdatetime() +'=='+str(symbol)+'==买入成功')
    return 'True'


def sell(symbol,percent,table):
    print(getdatetime()+'=='+str(symbol)+'==开始执行卖出任务...')
    exchange = login()
    sqldata = "SELECT id,amount,filled  from "+str(table)+" WHERE process='False' AND symbol='"+str(symbol)+"'"
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
    print('关联单:' + str(len(idlist)))
    wantprofit = (percent / 100) + 1 * sumamount
    orderbook = exchange.fetch_order_book(symbol=symbol)
    bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
    averageprice = (ask + bid) / 2
    profit = averageprice * sumfilled * 0.98
    print('当前均价:' + str(averageprice) + ',当前收益:' + str(profit) + ',预期收益:' + str(wantprofit))
    if profit > wantprofit:
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
            sqldata = "UPDATE "+str(table)+" set process = 'True' WHERE id='" + str(oid) + "' AND symbol='"+str(symbol)+"'"
            c.execute(sqldata)
            conn.commit()
            print('已更新订单' + str(oid) + '的状态')
        conn.close()
        print(getdatetime() +'=='+str(symbol)+ '==卖出成功')
        return 'True'
    conn.close()
    print(getdatetime() +'=='+str(symbol)+'==未达卖出条件')
    return 'False'






    #   print(json.dumps(exchange.fetchOrders(symbol=SYMBOL, params={'status': 1}), indent=4))
