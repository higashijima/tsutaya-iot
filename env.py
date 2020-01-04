import os

MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_USER = os.environ.get('MQTT_USER')
MQTT_PASS = os.environ.get('MQTT_PASSWORD')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')

FILE_BASES = {
    'A': 'america',
    'B': 'england',
    'C': 'india',
    'D': 'brasil'
}

TIME_ZONES = {
    'A': 'US/Eastern',
    'B': 'Europe/London',
    'C': 'Asia/Kolkata',
    'D': 'America/Sao_paulo',
    'tsutaya': 'Asia/Tokyo'
}

CAPITALS = {
    'A': 'ワシントンDC',
    'B': 'ロンドン',
    'C': 'ニューデリー',
    'D': 'ブラジリア',
    'tsutaya': '世田谷'
}

WEATHER_TABLE = {
    '01d': '晴れ',
    '01n': '晴れ',
    '02d': '曇り',
    '02n': '曇り',
    '03d': '曇り',
    '03n': '曇り',
    '04d': '曇り',
    '04n': '曇り',
    '09d': '雨',
    '09n': '雨',
    '10d': '雨',
    '10n': '雨',
    '11d': '雨',
    '11n': '雨',
    '13d': '雪',
    '13n': '雪',
    '50d': '霧',
    '50n': '霧',
    'error': 'エラー'
}

VOICE_TEXT = "${capital}の現在の時刻は${time}です。天気は${weather}、気温は${temp}度です"
WAV_FILE = '/tmp/voice.wav'
