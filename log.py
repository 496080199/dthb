# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler


log=logging.getLogger()
log.setLevel(logging.WARN)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
#h = RotatingFileHandler(filename='dthblog.log', maxBytes=50000000, backupCount=3, encoding='UTF-8')
h = TimedRotatingFileHandler(filename='dthblog.log', when='midnight', interval=1, backupCount=7, encoding='UTF-8')
h.setFormatter(fmt)
log.addHandler(h)

