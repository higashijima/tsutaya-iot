import argparse
import subprocess
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
if os.environ['DEBUG']!='':
  logger.setLevel(logging.DEBUG)

# テキストからwavファイルを作る
    
def create_wave(text, path):
  open_jtalk = ['open_jtalk']
  mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
  htsvoice = ['-m', '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']
  outwav = ['-ow', path]
  cmd = open_jtalk + mech + htsvoice + outwav
  logger.debug('command is %s', cmd)

  if isinstance(text, bytes):
    text = text.decode('utf-8')
 
  logger.debug('output text:[%s]', text)
  c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
  c.stdin.write(text)
  c.stdin.close()
  c.wait()
 
  return path

# wavファイルの再生
def play_wave(path):
  cmd = ['aplay', path]
  subprocess.call(cmd)

def jtalk(text, path='/tmp/talk.wav'):
  path = create_wave(text, path)
  play(path)

def replace_text(text, rmap):
  for k in rmap.keys():
    text = text.replace('${'+k+'}' , rmap[k])
  return text

def read_text(file):
  buf = open(file, "r")
  text = ""
  for line in buf:
    text += line

  buf.close()
  return text

if __name__ == '__main__':
  rmap = {'time': '12:30', 'weather': '曇り', 'temp': '32'}
  text = read_text("./america.txt")
  text = replace_text(text, rmap)

  logger.info(text)

  wavfile = '/tmp/voice.wav'
  play_wave(create_wave(text, wavfile))
  
  
