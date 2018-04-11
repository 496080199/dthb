# -*- coding: utf-8 -*-

from trade import *


def buycurrency():
    try:
        buy(QTUMSYMBOL, QTUMAMOUNT, QTUMTABLE)
        buy(EOSSYMBOL, EOSAMOUNT, EOSTABLE)
        buy(NEOSYMBOL, NEOAMOUNT, NEOTABLE)
        buy(ETHSYMBOL, ETHAMOUNT, ETHTABLE)
    except:
        pass
    return ''


def sellcurrency():
    try:
        sell(QTUMSYMBOL, QTUMPERCENT, QTUMTABLE)
        sell(EOSSYMBOL, EOSPERCENT, EOSTABLE)
        sell(ETHSYMBOL, ETHPERCENT, ETHTABLE)
    except:
        pass
    return ''
