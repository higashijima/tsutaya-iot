import datetime
from PIL import Image, ImageDraw, ImageFont
import unicornhathd as hat
import time
import os

DEFAULT_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
# アイコンIDと画像との対応表
ICON_TABLE = {
    '01d': 'clear-day.png',
    '01n': 'clear-night.png',
    '02d': 'partly-cloudy-day.png',
    '02n': 'partly-cloudy-night.png',
    '03d': 'cloudy.png',
    '03n': 'cloudy.png',
    '04d': 'cloudy.png',
    '04n': 'cloudy.png',
    '09d': 'rain.png',
    '09n': 'rain.png',
    '10d': 'rain.png',
    '10n': 'rain.png',
    '11d': 'rain.png',
    '11n': 'rain.png',
    '13d': 'snow.png',
    '13n': 'snow.png',
    '50d': 'fog.png',
    '50n': 'fog.png',
    'tsutaya': 'tsutaya.png',
    'A': 'america.png',
    'B': 'england.png',
    'C': 'india.png',
    'D': 'brasil.png',
    'demo': 'tsutaya.png',
    'error': 'error.png'
}

class unicorn:
  def __init__(self, font=DEFAULT_FONT):
    self.width, self.height = hat.get_shape()
    self.font = ImageFont.truetype(font, 6)
    hat.rotation(0)

  # ディスプレイクリア
  def init_disp(self):
    image = Image.new("RGB", (self.width, self.height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    return image, draw

  # ディスプレイ表示
  def draw_disp(self, image):
    for x in range(self.width):
      for y in range(self.height):
        r, g, b = image.getpixel((x, y))
        hat.set_pixel(self.width-x-1, y, r, g, b)
    hat.show()


  # 時刻表示
  def disp_clock(self, color):
    now = datetime.datetime.now()
    image, draw = self.init_disp()
    draw.text((0, -1), '{0:02}'.format(now.hour), fill=color, font=self.font)
    draw.text((0, 8), '{0:02}'.format(now.minute), fill=color, font=self.font)
    hat.clear()

    self.draw_disp(image)

  # テキスト表示
  def disp_text(self, draw, pos, text, color, fontsize=-1):
    if fontsize<0:
      font = self.font
    else:
      font = ImageFont.truetype(DEFAULT_FONT, fontsize)

    draw.text(pos, text, fill=color, font=font)

  # clear display
  def clear_disp(self):
    hat.clear()

  # アイコン表示
  def disp_icon(self, icon, wait=0.1, frame=-1):
    iconpath = self.get_icon_path(icon)
    image = Image.open(iconpath)
    for ox in range(int(image.size[0]/self.width) if frame<0 else 1):
      for oy in range(int(image.size[1]/self.height)):
        valid = False
        for x in range(self.width):
          for y in range(self.height):
            pixel = image.getpixel(((ox*self.width)+y, (oy*self.height)+x))
            r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
            if r or g or b:
              valid = True
            hat.set_pixel(x, y, r, g, b)
        if valid:
          hat.show()
          time.sleep(wait)

  def get_icon_path(self, id):
    current = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current, 'unicorn_mqtt_display', 'display', 'weather-icons', 'icons', ICON_TABLE[id])

if __name__=='__main__':
  u = unicorn()
  u.disp_icon('03d', 0.1, 1)
  time.sleep(1)
  u.disp_clock((0, 220, 220))
  time.sleep(0.5)
  u.disp_icon('tsutaya')
  for i in ICON_TABLE.keys():
    print('{0:}={1:}'.format(i, ICON_TABLE[i]))
    u.disp_icon(i, 0.01)
  time.sleep(0.4)
  image, draw = u.init_disp()
  u.disp_text(draw, (0,-1), '1023mb', (255,255,0))
  u.disp_text(draw, (0,8), '23C', (255,0,240))
  time.sleep(1)
  image, draw = u.init_disp()
  u.disp_text(draw, (0,-1), '11:02', (255,255,0))
  u.disp_text(draw, (0,8), 'UK', (255,0,240))

  hat.clear()
  u.draw_disp(image)
