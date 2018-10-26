# -*- coding: utf-8 -*-

from trade import *
from fxhgbi import *


def buycurrency():
    if belowavg():
        log.warn('低于300日均线买入')
        #buy(QTUMSYMBOL, QTUMAMOUNT * 2, QTUMTABLE)
        #buy(EOSSYMBOL, EOSAMOUNT * 2, EOSTABLE)
        buy(NEOSYMBOL, NEOAMOUNT * 2, NEOTABLE)
    elif overavg():
        log.warn('超高于300日均线不买入')
        pass
    else:
        log.warn('正常买入')
        #buy(QTUMSYMBOL, QTUMAMOUNT, QTUMTABLE)
        #buy(EOSSYMBOL, EOSAMOUNT, EOSTABLE)
        buy(NEOSYMBOL, NEOAMOUNT, NEOTABLE)

    return ''


def sellcurrency():
    sell(QTUMSYMBOL, QTUMPERCENT, QTUMTABLE)
    #sell(EOSSYMBOL, EOSPERCENT, EOSTABLE)
    #sell(NEOSYMBOL, NEOPERCENT, NEOTABLE)
    sell(ETHSYMBOL, ETHPERCENT, ETHTABLE)
    #sell(XRPSYMBOL, XRPPERCENT, XRPTABLE)
    checkbalance()
    return ''


def hardbuycurrency():
    if belowavg():
        log.warn('低于300日均线买入')
        buy(ETHSYMBOL, ETHAMOUNT*2, ETHTABLE)
        #buy(XRPSYMBOL, XRPAMOUNT*2, XRPTABLE)
    elif overavg():
        log.warn('超高于300日均线不买入')
        pass
    else:
        log.warn('正常买入')
        buy(ETHSYMBOL, ETHAMOUNT, ETHTABLE)
        #buy(XRPSYMBOL, XRPAMOUNT, XRPTABLE)
