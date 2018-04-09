# -*- coding: utf-8 -*-
import ccxt,json
from config import *

exchange = ccxt.huobipro()
exchange.apiKey = ACCKEY
exchange.secret = SECKEY

print(json.dumps(exchange.fetch_orders(symbol=NEOSYMBOL, params={'status': 1, 'side': 'sell'}), indent=4))
#print(json.dumps(exchange.fetch_order(symbol=SYMBOL, id="2624924134"), indent=4))
#if exchange.fetch_order(symbol=SYMBOL, id="2624924134")['status'] == 'closed':
#    print('True')

#balance=exchange.fetch_balance()['info']['data']['list']

#and i['type'] == 'trade'
#for i in balance:
 #   if i['currency'] == 'qtum' :
  #     print('可用QTUM:'+i['balance'])