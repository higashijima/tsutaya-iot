import argparse
import subprocess
from logging import getLogger, INFO, DEBUG
logger = getLogger(__name__)
logger.setLevel(INFO)
import os

class voice:
  def __init__(self, enc='utf-8', mechpath='/var/lib/mecab/dic/open-jtalk/naist-jdic', htspath='/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'):
    self.mechpath = mechpath
    self.htspath = htspath

# テキストからwavファイルを作る
    
  def create_wave(self, text, path):
    if isinstance(text, bytes):
      text = text.decode('utf-8')
    text = text.encode('utf-8')
 
    # コマンドラインとオプション
    open_jtalk = ['open_jtalk']
    mech = ['-x', self.mechpath]
    htsvoice = ['-m', self.htspath]
    outwav = ['-ow', path]

    cmd = open_jtalk + mech + htsvoice + outwav
    logger.debug('command is %s', cmd)

    logger.debug('output text:[%s]', text)
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(text)
    c.stdin.close()
    c.wait()
 
    return path

# wavファイルの再生
  def play_wave(self, path):
    cmd = ['aplay', path]
    subprocess.call(cmd)

  def jtalk(self, text, path='/tmp/talk.wav'):
    path = self.create_wave(text, path)
    play(path)

  def replace_text(self, text, rmap):
    for k in rmap.keys():
      text = text.replace('${'+k+'}' , rmap[k])
    return text

  def read_text(self, file):
    buf = open(file, "r")
    text = ""
    for line in buf:
      text += line

    buf.close()
    return ''.join(text.splitlines())

if __name__ == '__main__':
  v = voice()
  rmap = {'time': '12:30', 'weather': '曇り', 'temp': '32'}
  text = v.read_text("./america.txt")
  text = v.replace_text(text, rmap)

  logger.info(text)

  wavfile = '/tmp/voice.wav'
  v.play_wave(v.create_wave(text, wavfile))
  
  
