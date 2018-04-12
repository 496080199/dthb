# -*- coding: utf-8 -*-

from trade import *


def buycurrency():
    try:
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
        buy(ETHSYMBOL, ETHAMOUNT, ETHTABLE)
        buy(XRPSYMBOL, XRPAMOUNT, XRPTABLE)
    except:
        log.warn('异常退出')
        pass



