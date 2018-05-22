# -*- coding: utf-8 -*-

from trade import *
from fxhgbi import *


def buycurrency():
    try:
        if belowavg():
            buy(QTUMSYMBOL, QTUMAMOUNT * 2, QTUMTABLE)
            buy(EOSSYMBOL, EOSAMOUNT * 2, EOSTABLE)
            buy(NEOSYMBOL, NEOAMOUNT * 2, NEOTABLE)
        else:
            buy(QTUMSYMBOL, QTUMAMOUNT, QTUMTABLE)
            buy(EOSSYMBOL, EOSAMOUNT, EOSTABLE)
            buy(NEOSYMBOL, NEOAMOUNT, NEOTABLE)
    except:
        log.warn('异常退出')
        pass
    return ''


def sellcurrency():
    try:
        sell(QTUMSYMBOL, QTUMPERCENT, QTUMTABLE)
        sell(EOSSYMBOL, EOSPERCENT, EOSTABLE)
        sell(NEOSYMBOL, NEOPERCENT, NEOTABLE)
        sell(ETHSYMBOL, ETHPERCENT, ETHTABLE)
        sell(XRPSYMBOL, XRPPERCENT, XRPTABLE)
    except:
        log.warn('异常退出')
        pass
    return ''


def hardbuycurrency():
    try:
        if belowavg():
            buy(ETHSYMBOL, ETHAMOUNT*2, ETHTABLE)
            buy(XRPSYMBOL, XRPAMOUNT*2, XRPTABLE)
        else:
            buy(ETHSYMBOL, ETHAMOUNT, ETHTABLE)
            buy(XRPSYMBOL, XRPAMOUNT, XRPTABLE)
    except:
        log.warn('异常退出')
        pass
