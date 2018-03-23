# -*- coding: utf-8 -*-
import ccxt,json
from config import *

exchange = ccxt.huobipro()
exchange.apiKey = ACCKEY
exchange.secret = SECKEY

print(json.dumps(exchange.fetch_orders(symbol=SYMBOL, params={'status': 1}), indent=4))
#print(json.dumps(exchange.fetch_order(symbol=SYMBOL, id="2624924134"), indent=4))
#if exchange.fetch_order(symbol=SYMBOL, id="2624924134")['status'] == 'closed':
#    print('True')