# -*- coding: utf-8 -*-

from trade import *


def buycurrency():
    try:
        buy(QTUMSYMBOL, QTUMAMOUNT, QTUMTABLE)
        buy(EOSSYMBOL, EOSAMOUNT, EOSTABLE)
    except:
        pass
    return ''


def sellcurrency():
    try:
        sell(QTUMSYMBOL, QTUMPERCENT, QTUMTABLE)
        sell(EOSSYMBOL, EOSPERCENT, EOSTABLE)
    except:
        pass
    return ''
