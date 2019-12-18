from logging import getLogger, DEBUG, INFO, StreamHandler
import sys
import os
logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(StreamHandler(stream=sys.stdout))
import pytz

import paho.mqtt.client as mqtt
from unicornhat import unicorn
import unicornhathd as hat
import datetime
import time
import json
from threading import Thread, Event
import weather as w

MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_USER = os.environ.get('MQTT_USER')
MQTT_PASS = os.environ.get('MQTT_PASSWORD')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
DISP_MODE = os.environ.get('DISP_MODE')

files = {'A': 'america', 'B': 'england', 'C': 'india', 'D': 'brasil', 'tsutaya': 'tsutaya'}
timezone = {'A': 'US/Eastern', 'B': 'Europe/London', 'C': 'Asia/Kolkata', 'D': 'America/Sao_paulo', 'tsutaya': 'Asia/Tokyo'}
u = unicorn()


def change(mode):
    if mode not in ('demo', 'touch'):
        logger.warn('invalid mode(%s)', mode)
        return false

    logger.debug('mode is (%s)', mode)

    func = None
    if mode == 'demo':
        func = demo_loop
    elif mode == 'touch':
        func == touch
    else:
        logger.error('cannot get function')
        return False

    event.set()
    time.sleep(1)
    envent.clear()

    driver = Thread(target=func, args=(event,))
    driver.daemon = True
    driver.start()

    return True


def start():
    logger.debug('display initial function')

def disp_msg(event, temp, press, icon):
    logger.debug('event(%s) temp(%s) press(%s) icon(%s)', event, temp, press, icon)
    if DISP_MODE == 'flag':
        u.disp_icon(event)

    if DISP_MODE == 'temp':
        logger.debug('%s', timezone[event])
        now = datetime.datetime.now(pytz.timezone(timezone[event])) 
        now_hour = "{0:02d}".format(now.hour)
        now_min = "{0:02d}".format(now.minute)
        image, draw = u.init_disp()
        u.clear_disp()
        u.disp_text(draw, (2, -1), now_hour, (255,255,0), 7)
        u.disp_text(draw, (6, 4), now_min, (255,127,0), 7)
        u.disp_text(draw, (0, 9), temp+'℃', (255,0,255), 7)
        u.draw_disp(image)

    if DISP_MODE == 'weather':
        u.disp_icon(icon)
    

def main():
    # debug mode when environmet set DEBUG 
    if os.environ.get('DEBUG', None):
        logger.setLevel(DEBUG)


    topic = os.environ.get('MQTT_TOPIC', '#')
    icon_tokyo, temp_tokyo, press_tokyo = w.getWeatherInfo('tsutaya')
    disp_msg('tsutaya', '{0:d}'.format(int(temp_tokyo)), press_tokyo, icon_tokyo)

    def on_connect(client, userdata, flags, respons_code):
        logger.info('subscribe %s', topic)
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        try:
            retain = 'Yes' if msg.retain else 'No'
            sendTime = msg.timestamp
            qos = msg.qos
            topic = msg.topic
            logger.debug(msg.payload)
            if msg == None:
                payload = {
                'error': True,
                'results': {
                    'event': 'tsutaya',
                    'weather': '',
                    'temperature': '',
                    'pressure': '',
                }
            }
            else:
                payload = json.loads(msg.payload.decode('utf-8'))
        
            logger.debug('%s retain=%s qos=%s [%s] %s', sendTime, retain, qos, topic, payload)
            logger.debug(payload['results']['event'])
            event = payload['results']['event']
            icon = payload['results']['weather']
            temperature = payload['results']['temperature']
            pressure = payload['results']['pressure']

            logger.debug('disp touch')
            disp_msg(event, temperature, pressure, icon)
            time.sleep(3)
            logger.debug('disp tokyo')
            icon_tokyo, temp_tokyo, press_tokyo = w.getWeatherInfo('tsutaya')
            temperature = '{0:d}'.format(int(temp_tokyo))
            pressure = '{0:d}'.format(press_tokyo)
            disp_msg('tsutaya', temperature, pressure, icon)
            #disp_msg('tsutaya', '{0:d}'.format(int(temp_tokyo)), press_tokyo, icon_tokyo)

        except Exception as e:
            logger.exception(e)

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.username_pw_set(MQTT_USER, password=MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT)

    try:
        client.loop_forever()
        demo_loop()
        
    finally:
        client.disconnect()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('bye.')
        sys.exit(0)

