from logging import getLogger, DEBUG, INFO, StreamHandler
import sys
import os
logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(StreamHandler(stream=sys.stdout))

import paho.mqtt.client as mqtt
from unicornhat import unicorn
import unicornhathd as hat
import datetime
import time

MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_USER = os.environ.get('MQTT_USER')
MQTT_PASS = os.environ.get('MQTT_PASS')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
DISP_MODE = os.environ.get('DISP_MODE')

files = {'A': 'america', 'B': 'england', 'C': 'india', 'D': 'brasil'}


def main():
    # debug mode when environmet set DEBUG 
    if os.environ.get('DEBUG', None):
        logger.setLevel(DEBUG)

    topic = os.environ.get('MQTT_TOPIC', '#')
    u = unicorn()

    def on_connect(client, userdata, flags, respons_code):
        logger.info('subscribe %s', topic)
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        try:
            retain = 'Yes' if msg.retain else 'No'
            sendTime = msg.timestamp
            qos = msg.qos
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            logger.debug('%s retain=%s qos=%s [%s] %s', sendTime, retain, qos, topic, payload)
            rmap = {'time': '12:30', 'weather': '曇り', 'temp': '32'}
            if DISP_MODE == 'flag':
                u.disp_icon('./icons/'+files[payload]+'.png')
            if DISP_MODE == 'temp':
                now = "{0:%H:%M}".format(datetime.datetime.now())
                temp = '13C'
                image, draw = u.init_disp()
                
                u.disp_text(draw, (0, -1), now, (255,255,0))
                u.disp_text(draw, (0, 8), temp, (255,0,255))
                u.draw_disp(image)
            if DISP_MODE == 'weather':
                weather = 'cloudy'
                u.disp_icon('./icons/weather/'+weather+'.png')

        except Exception as e:
            logger.exception(e)

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.username_pw_set(MQTT_USER, password=MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT)

    try:
        client.loop_forever()
    finally:
        client.disconnect()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('bye.')
        sys.exit(0)

