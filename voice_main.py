from logging import getLogger, DEBUG, INFO, StreamHandler
import sys
import os
logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(StreamHandler(stream=sys.stdout))

import paho.mqtt.client as mqtt
from voicekit import voice

MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_USER = os.environ.get('MQTT_USER')
MQTT_PASS = os.environ.get('MQTT_PASS')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')

files = {'A': 'america', 'B': 'england', 'C': 'india', 'D': 'brasil'}
countries = {'A': 'US/Eastern', 'B': 'Europe/London', 'C': 'Asia/Kolkata', 'D': 'America/Sao_paulo'}
# weathers = {'A': }

def main():
    # debug mode when environmet set DEBUG 
    if os.environ.get('DEBUG', None):
        logger.setLevel(DEBUG)

    topic = os.environ.get('MQTT_TOPIC', '#')
    v = voice()

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
            _, localtime = v.get_time()
            rmap = {'time': localtime, 'weather': '曇り', 'temp': '32'}
            text = v.replace_text(v.read_text("./"+files[payload]+".txt"), rmap)
            wavfile = '/tmp/voice.wav'
            v.play_wave(v.create_wave(text,wavfile))

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

