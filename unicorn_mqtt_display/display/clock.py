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

ICON_TABLE = {
    '01d': 'clear-day.png',
    '01n': 'clear-night.png',
    '02d': 'partly-cloudy-day.png',
    '02n': 'partly-cloudy-night.png',
    '03d': 'cloudy.png',
    '03n': 'cloudy.png',
    '04d': 'cloudy.png',
    '04n': 'cloudy.png',
    '09d': 'rain.png',
    '09n': 'rain.png',
    '10d': 'rain.png',
    '10n': 'rain.png',
    '11d': 'rain.png',
    '11n': 'rain.png',
    '13d': 'snow.png',
    '13n': 'snow.png',
    '50d': 'fog.png',
    '50n': 'fog.png',
    'A': 'america.png',
    'D': 'brasil.png',
    'B': 'england.png',
    'C': 'india.png',
    'tsutaya': 'tsutaya.png',
    'error': 'error.png'
}

files = {'A': 'america', 'B': 'england', 'C': 'india', 'D': 'brasil', 'tsutaya': 'tsutaya'}
timezone = {'A': 'US/Eastern', 'B': 'Europe/London', 'C': 'Asia/Kolkata', 'D': 'America/Sao_paulo', 'tsutaya': 'Asia/Tokyo'}
DISP_MODE = os.environ.get('DISP_MODE')
width, height = unicornhathd.get_shape()
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
        if msg == None:
            wait = 0.1
            flag = 'tsutaya'
            icon, temperature, _  = wi.getWeatherInfo(flag)
        else:
            payload = json.loads(msg.payload.decode('utf-8'))
            flag = payload['results']['event']
            icon = payload['results']['weather']
            temperature = payload['results']['temperature']
            wait = 3
            zone = timezone[flag]

        temp = "{0:.0f}".format(temperature)
    
        if DISP_MODE == 'flag':
            u.disp_icon(flag, 0, 1)

        if DISP_MODE == 'temp':
            now_hour = "{0:%H}".format(datetime.datetime.now(zone))
            now_min = "{0:%m}".format(datetime.datetime.now(zone))
            image, draw = u.init_disp()
            u.clear_disp()
            u.disp_text(draw, (2, -1), now_hour, (0,255,255), 7)
            u.disp_text(draw, (6, 4), now_min, (0,127,255), 7)
            u.disp_text(draw, (0, 9), temp+'℃', (0,255,255), 7)
            u.draw_disp(image)

        if DISP_MODE == 'weather':
            u.disp_icon(icon)

        time.sleep(wait)
        unicornhathd.clear()

    logger.debug('clock loop end.')
