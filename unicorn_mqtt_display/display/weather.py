#!/usr/bin/env python3
# coding: utf-8

from logging import getLogger
logger = getLogger(__name__)

from .unicorn_weather_official_icon import getWeather, filterNearstWeather
from PIL import Image
import datetime
import unicornhathd
import requests
import time
import os
import weatherinfo as wi
import json

APIKEY = os.environ.get('OPENWEATHER_API_KEY')
DEFAULT_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

CYCLE_TIME = 0.5

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

files = {'A': 'america', 'B': 'england', 'C': 'india', 'D': 'brasil'}
timezone = {'A': 'US/Eastern', 'B': 'Europe/London', 'C': 'Asia/Kolkata', 'D': 'America/Sao_paulo'}
DISP_MODE = os.environ.get('DISP_MODE')

CURRENT_DIR = os.path.dirname(__file__)
WEATHER_ICONS_DIRECTORY = os.path.join(CURRENT_DIR, 'weather-icons', 'icons')
if not os.path.exists(WEATHER_ICONS_DIRECTORY):
    raise RuntimeError('Icon directory not found. (%s)', WEATHER_ICONS_DIRECTORY)

width, height = unicornhathd.get_shape()



def main(event, msg):
    """
    メイン処理
    これをループし続ける
    """
    logger.info("display touch mode")

    payload = json.loads(msg.payload.decode('utf-8'))

    flag = payload['results']['event']
    icon = payload['results']['weather']
    temperature = payload['results']['temperature']

    # 現在時刻の取得
    now = datetime.datetime.now()

    # datetimeオブジェクトをUnixTimeに変換し、ターゲット時間を作る
    # ターゲットを2時間先とする
    target_timestamp = now.timestamp()

    try:
        unicornhathd.clear()
        icon, temperature, _ = wi.getWeatherInfo(flag)
        logger.debug('weather is %s', icon)

        temp = "{0:.0f}".format(temperature)
        if DISP_MODE == 'flag':
            u.disp_icon(flag)

        if DISP_MODE == 'temp':
            now_hour = "{0:%H}".format(datetime.datetime.now(timezone[flag]))
            now_min = "{0:%m}".format(datetime.datetime.now(timezone[flag]))
            image, draw = u.init_disp()
            u.clear_disp()
            u.disp_text(draw, (2, -1), now_hour, (0,255,255), 7)
            u.disp_text(draw, (6, 4), now_min, (0,127,255), 7)
            u.disp_text(draw, (0, 9), temp+'℃', (0,255,255), 7)
            u.draw_disp(image)

        if DISP_MODE == 'weather':
            u.disp_icon(icon)

        time.sleep(5)


    except requests.exceptions.ConnectionError as e:
        logger.exception(e)
        time.sleep(30 * 3)

    except KeyError:
        time.sleep(30 * 3)
        return

    logger.debug('start write icon.')

    for i in range(0, 300):
        if event.is_set():
            break

    logger.debug('end of one cicle.')

def loop(event, msg):
    unicornhathd.rotation(0)

    logger.debug('weather loop stert.')
    while not event.is_set():
        main(event, msg)

    logger.debug('weather loop end.')


if __name__ == '__main__':
    """
    この書き方をしているのは
    これをライブラリとしてロードできるようにするため。
    https://docs.python.jp/3/library/__main__.html
    """

    # ロガーの設定
    # スクリプトとして動作する場合のみ出力ハンドラを追加する。
    from logging import StreamHandler, INFO, DEBUG, Formatter
    import sys

    # 環境変数DEBUGによってロギングレベルを変更する
    if os.environ.get('DEBUG', None):
        logger.setLevel(DEBUG)
    else:
        logger.setLevel(INFO)

    # StreamHandlerはそのまま標準出力として出力する。
    # つまりprint()と同様の動きをする
    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter('[%(levelname)s] %(asctime)s %(name)s %(message)s'))
    logger.addHandler(handler)

    logger.info('start application.')
    logger.info('city is %s', CITY)

    unicornhathd.brightness(0.5)
    unicornhathd.rotation(90)

    # ここがメイン処理。
    # main()をひたすらループさせる。
    # finally
    try:
        while True:
            main()

    # Ctrl+C時に起きる例外を取得し、エラーメッセージが出ないようにする。
    except KeyboardInterrupt:
        logger.info('detect sigterm. goodbye.')

    # finallyは例外が出ようが出まいが終了時に必ず動作される。
    # ここでは、unicornhathdの終了処理を行わさせている。
    finally:
        unicornhathd.off()

