import paho.mqtt.client as mqtt
import os

class mqtt:
  def __init__(self, host, user, password, port):
    self.__host = host
    self.__user = user
    self.__password = password
    self.__port = port
    self.client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.username_pw_set(self.__user, password=self.__password)

if __name__ == '__main__':
  host = os.environ.get('MQTT_HOST')
  user = os.environ.get('MQTT_USER')
  password = os.environ.get('MQTT_PASSWORD')
  port = int(os.environ.get('MMQTT_PORT')
  
