# -*- coding: utf-8 -*-

from trade import *


def buycurrency():
    buy(QTUMSYMBOL, QTUMAMOUNT, QTUMTABLE)
    buy(EOSSYMBOL, EOSAMOUNT, EOSTABLE)
    return ''


def sellcurrency():
    sell(QTUMSYMBOL, QTUMPERCENT, QTUMTABLE)
    sell(EOSSYMBOL, EOSPERCENT, EOSTABLE)
    return ''
