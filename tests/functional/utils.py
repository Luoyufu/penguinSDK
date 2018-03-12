# -*- coding: utf-8 -*-

from datetime import datetime


def now_str():
    now = datetime.now()

    return now.strftime('%y%m%d%H%M')
