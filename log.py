# -*- coding: utf-8 -*-

import logging

log=logging.getLogger()
log.setLevel(logging.WARN)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.FileHandler(filename='dthblog.log', encoding='UTF-8')
h.setFormatter(fmt)
log.addHandler(h)

