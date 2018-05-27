# -*- coding: utf-8 -*-

from trade import *
from fxhgbi import *


def buycurrency():
    try:
        if belowavg():
            log.warn('低于300日均线买入')
            buy(QTUMSYMBOL, QTUMAMOUNT * 2, QTUMTABLE)
            buy(EOSSYMBOL, EOSAMOUNT * 2, EOSTABLE)
            buy(NEOSYMBOL, NEOAMOUNT * 2, NEOTABLE)
        elif overavg():
            log.warn('超高于300日均线不买入')
            pass
        else:
            log.warn('正常买入')
            buy(QTUMSYMBOL, QTUMAMOUNT, QTUMTABLE)
            buy(EOSSYMBOL, EOSAMOUNT, EOSTABLE)
            buy(NEOSYMBOL, NEOAMOUNT, NEOTABLE)
    except Exception as e:

        log.warn('买入异常退出:'+str(e))
        pass
    return ''


def sellcurrency():
    try:
        sell(QTUMSYMBOL, QTUMPERCENT, QTUMTABLE)
        sell(EOSSYMBOL, EOSPERCENT, EOSTABLE)
        sell(NEOSYMBOL, NEOPERCENT, NEOTABLE)
        sell(ETHSYMBOL, ETHPERCENT, ETHTABLE)
        sell(XRPSYMBOL, XRPPERCENT, XRPTABLE)
    except Exception as e:
        log.warn('卖出异常退出:'+str(e))
        pass
    return ''


def hardbuycurrency():
    try:
        if belowavg():
            log.warn('低于300日均线买入')
            buy(ETHSYMBOL, ETHAMOUNT*2, ETHTABLE)
            buy(XRPSYMBOL, XRPAMOUNT*2, XRPTABLE)
        elif overavg():
            log.warn('超高于300日均线不买入')
            pass
        else:
            log.warn('正常买入')
            buy(ETHSYMBOL, ETHAMOUNT, ETHTABLE)
            buy(XRPSYMBOL, XRPAMOUNT, XRPTABLE)
    except Exception as e:
        log.warn('硬买入异常退出:'+str(e))
        pass
