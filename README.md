# tsutaya-iot
for voicekit

sudo apt update && sudo apt-get install -y python3 python3-pip &&
sudo pip3 install paho.mqtt
女性の声(メイちゃん)
https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip
cd /usr/share/hts-voice
sudo mkdir mei
sudo wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip
sudo unzip MMDAgent_Example-1.7.zip
sudo mv MMDAgent_Example-1.7/Voice/mei/*.htsvoice mei
