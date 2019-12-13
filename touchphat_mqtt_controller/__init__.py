# coding: utf-8

"""
    TouchPhat部分の制御を行う。
"""

import touchphat
import os
import time
from threading import Lock
import json

# 別途ファイルで定義したMQTTクライアントをインポートする
from .mqtt import client, start

# 変更要求をパブリッシュするトピックを作成する
TARGET_NAME = os.environ.get('MQTT_TARGET_NAME')
TOPIC = 'cmnd/' + TARGET_NAME + '/display/change'

# ロックオブジェクトの作成
# https://docs.python.jp/3/library/threading.html#lock-objects
lock = Lock()

def animation():
    """
        動作開始時のアニメーション
    """
    touchphat.all_off()
    for i in range(1, 7):
        touchphat.led_on(i)
        time.sleep(0.05)
    for i in range(1, 7):
        touchphat.led_off(i)
        time.sleep(0.05)

def blink(key):
    """
        動作受付時の点滅アニメーション
    """
    touchphat.all_off()
    for i in range(0, 3):
        touchphat.led_off(key)
        time.sleep(0.1)
        touchphat.led_on(key)
        time.sleep(0.1)
    touchphat.all_off()

def beep(key):
    """
        動作非受付時のアニメーション
    """
    touchphat.all_off()
    touchphat.led_on(key)
    time.sleep(0.9)
    touchphat.all_off()

def getPressure(ev):
    return 1022

def getWeather(ev):
    return 'cloudy'

def getTempreture(ev):
    return 13.54

@touchphat.on_release(['Back','A', 'B', 'C', 'D','Enter'])
def handle_touch(event):
    """
        TochPhatのボタン操作時のコールバック
    """
    # Lockオブジェクトを使用して排他制御を行う
    with lock:
        payload_json = {
            'error': True,
            'results': {
                'event': event.name,
                'weather': getWeather(event.name),
                'tempture': getTempreture(event.name),
                'pressure': getPressure(event.name),
            }
        }
        if event.name is not None:
            client.publish(
                    topic=TOPIC,
                    payload=json.dumps(payload_json)
                )
            blink(event.name)

        else:
            beep(event.name)

def main():
    """
        メイン関数
        ここで動かしているstartは上でインポートしたMQTTの接続開始関数
    """
    animation()
    start()
