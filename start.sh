#!/bin/bash

case $(hostname) in
t-iot-voice)script=voice;;
t-iot-touch*)script=touch;;
t-iot-unicorn*)script=unicorn;;
t-iot-enviro*)script=enviro;;
*) echo "no script execute..."
exit 1;;
python3 ${script}_main.py
