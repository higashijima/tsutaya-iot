# tsutaya-iot
for voicekit

```
sudo apt update && sudo apt-get install -y python3 python3-pip 
sudo pip3 -y install paho.mqtt
```

# unicorn-mqtt

MQTT通信を使い、TouchPhatを刺したRaspberryPiでUnicornHatHDを刺したRaspberryPiの表示を制御するサンプル。


## 概要

このスクリプトはMQTT通信を用いてTouchPhatのボタン操作でUnicornHatHDの表示を時計、天気予報と切り替え動作を行うサンプルです。

MQTTブローカーは別途用意する必要がありますが、CoudMQTTサービスを使うことを推奨します。  
<https://www.cloudmqtt.com>



## 環境構築
それぞれ以下のコマンドを使用して必須パッケージをインストールします。

### UnicornHatHD側

```shell
$ sudo raspi-config # SPIを有効にする
$ sudo apt-get install python3-pip python3-dev python3-spidev python3-pil python3-numpy -y
$ sudo apt-get install ttf-dejavu fonts-takao -y
$ sudo pip3 install unicornhathd paho-mqtt requests
```

ライブラリ内の `unicorn_mqtt_display/display` ディレクトリ上に公式ライブラリの `examples` 上にある
`weather-icons`　ディレクトリをコピーする必要があります 

<https://github.com/pimoroni/unicorn-hat-hd/tree/master/examples/weather-icons>



### TouchPhat側

```shell
$ sudo raspi-config # I2Cを有効にする
$ sudo apt-get install python3-pip python3-dev python3-smbus -y
$ sudo pip3 install touchphat paho-mqtt
```

## ライブラリへのリンク

- CloudMQTT - <https://www.cloudmqtt.com>
- UnicornHatHD - <https://github.com/pimoroni/unicorn-hat-hd>
- touchPhat - <https://github.com/pimoroni/touch-phat>
- paho.mqtt - <https://www.eclipse.org/paho/clients/python/docs/>
- openWeather - <https://openweathermap.org/api>
- requests - <https://requests-docs-ja.readthedocs.io/en/latest/>

sudo apt update && sudo apt-get install -y python3 python3-pip &&
sudo pip3 install paho.mqtt
```

女性の声(メイちゃん)
https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip

```
cd /usr/share/hts-voice
sudo mkdir mei
sudo wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip
sudo unzip MMDAgent_Example-1.7.zip
sudo mv MMDAgent_Example-1.7/Voice/mei/*.htsvoice mei
```
