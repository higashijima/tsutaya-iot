#!/usr/bin/env python3
# coding: utf-8

"""
    時計表示スクリプト
    中身はいつか作ったものと同様ですが、
    並列処理を実現するために少し手直しを加えています。
"""

from logging import getLogger
logger = getLogger(__name__)

logger.debug('loaded')

import datetime
from PIL import Image, ImageDraw, ImageFont
from unicornhat import unicorn
import os
import unicornhathd
import time
import weatherinfo as wi

COLOR = (200, 0, 0)

width, height = unicornhathd.get_shape()
DISP_MODE = os.environ.get('DISP_MODE')
u = unicorn()


# 無限ループ
def loop(event, msg):
    """
        ループ関数
        引数にEventオブジェクトをとり、終了イベントを受け取れるように改変を加えている。
    """
    logger.debug('clock loop start.')

    unicornhathd.rotation(0)

    # ループ条件をeventオブジェクトがイベントを受け取っていないことにしている
    # eventがセットされるとループを終了する
    while not event.is_set():
        icon, temperature, _  = wi.getWeatherInfo('tsutaya')
        temp = "{0:.0f}".format(temperature)
        if DISP_MODE == 'flag':
            u.disp_icon('tsutaya', 0, 1)

        if DISP_MODE == 'temp':
            now_hour = "{0:%H}".format(datetime.datetime.now())
            now_min = "{0:%m}".format(datetime.datetime.now())
            image, draw = u.init_disp()
            u.clear_disp()
            u.disp_text(draw, (2, -1), now_hour, (0,255,255), 7)
            u.disp_text(draw, (6, 4), now_min, (0,127,255), 7)
            u.disp_text(draw, (0, 9), temp+'℃', (0,255,255), 7)
            u.draw_disp(image)

        if DISP_MODE == 'weather':
            u.disp_icon(icon)

        unicornhathd.clear()

    logger.debug('clock loop end.')
