# coding: utf-8

"""
    weather get module
"""

import os
import time
import requests
import json
import datetime

# 別途ファイルで定義したMQTTクライアントをインポートする

# Openweathermap API constants
APIBASE = 'https://api.openweathermap.org/data/2.5/forecast'
ICON_PATH = 'http://openweathermap.org/img/w'
APIKEY = os.environ['OPENWEATHER_API_KEY']

# Openweathermapの気温の値はK(ケルビン、絶対温度)なので摂氏に直すためには273.15℃引く
ABSOLUTE_TEMP = 273.15

# ロックオブジェクトの作成
# https://docs.python.jp/3/library/threading.html#lock-objects

def filterNearstWeather(weathers, date):
    """
    openWeatherレスポンスのweatherリストから指定時刻に一番近いものを選択する
    Noneが帰る場合もある
    """
    
    # 計算用のターゲット時間のタイムスタンプを作る。
    # 引数がdatetimeオブジェクトだった場合はそこからunixtimeを取得する
    # それ以外の場合はunixtimeが渡されたとみなす。
    # こうすることで引数dateはunixtime、datetimeオブジェクトのどちらにも対応でき、可用性が上がる
    if isinstance(date, datetime.datetime):
        target_timestamp = date.timestamp()
    else:
        target_timestamp = date

    # 天気予報情報を1つづつ確認してターゲット時間と合致するかを試す
    # 今回の合致条件は、予報の時間がターゲットよりも後かつターゲットから2時間以内であること
    # これを見つけ次第ループ処理を解除する
    weather = None
    for i in weathers:
        if i['dt'] > target_timestamp and abs(i['dt'] - target_timestamp) <= 3600 * 3:
            weather = i
            break

    return weather

def getWeatherInfo(ev):
    cities = {'A': 'Washington', 'B': 'London', 'C': 'New Delhi', 'D': 'Brasilia', 'tsutaya': 'Setagaya'}

    payload = {
        'APIKEY': APIKEY,
        'q': cities[ev]
    }
    r = requests.get(
        APIBASE,
        params=payload
    )
    w = filterNearstWeather(r.json()['list'], datetime.datetime.now().timestamp())
    if r.ok:
        return w['weather'][0]['icon'], w['main']['temp'] - ABSOLUTE_TEMP, w['main']['pressure']
    else:
        return 'error', 'XX', 'XX'

if __name__ == '__main__':
    for a in ('A', 'B', 'C', 'D', 'demo'):
        weather, temperature, pressure  = getWeatherInfo(a)
        print(weather)
        print(temperature)
        print(pressure)
    

