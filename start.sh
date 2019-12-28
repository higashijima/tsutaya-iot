#!/bin/bash

export MQTT_HOST=m10.cloudmqtt.com
export MQTT_USER=juhtilne 
export MQTT_PASSWORD=GKqNGG_jAh9N 
export MQTT_PORT=11515
export EXEC_MAIN=voice
script=${EXEC_MAIN}
python3 ${script}_main.py
