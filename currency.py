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
    except:
        log.warn('异常退出')
        pass
    return ''

def hardbuycurrency():
    try:
        buy(ETHSYMBOL, ETHAMOUNT, ETHTABLE)
    except:
        log.warn('异常退出')
        pass
def hardsellcurrency():
    try:
        sell(ETHSYMBOL, ETHPERCENT, ETHTABLE)
    except:
        log.warn('异常退出')
        pass


