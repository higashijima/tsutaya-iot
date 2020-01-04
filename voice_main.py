from logging import getLogger, DEBUG, INFO, StreamHandler
import sys
import os
logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(StreamHandler(stream=sys.stdout))

import paho.mqtt.client as mqtt
from voicekit import voice
import json
from threading import Thread
import env

def main():
    # debug mode when environmet set DEBUG 
    if os.environ.get('DEBUG', None):
        logger.setLevel(DEBUG)

    v = voice()

    def on_connect(client, userdata, flags, respons_code):
        logger.info('subscribe %s', topic)
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        logger.debug('on message')
        try:
            retain = 'Yes' if msg.retain else 'No'
            sendTime = msg.timestamp
            qos = msg.qos
            topic = msg.topic
            payload = json.loads(msg.payload.decode('utf-8'))
            event = payload['results']['event']
            logger.debug('%s retain=%s qos=%s [%s] %s', sendTime, retain, qos, topic, payload)
            _, localtime = v.get_time(timezone[payload['results']['event']])
            temp = payload['results']['temperature']
            weather = WEATHER_TABLE[payload['results']['weather']]
            capital = capitals[event]
            rmap = {'capital': capital, 'time': localtime, 'weather': weather, 'temp': temp}
            text = v.replace_text(env.VOICE_TEXT, rmap)
            logger.debug(text)
            thread1 = Thread(target=v.create_wave, args=(text, env.WAV_FILE,))
            thread1.start()
            v.play_wave("./"+files[event]+".wav")
            v.play_wave(env.WAV_FILE)
            os.remove(env.WAV_FILE)

        except Exception as e:
            logger.exception(e)

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.username_pw_set(env.MQTT_USER, password=env.MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(env.MQTT_HOST, env.MQTT_PORT)

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

