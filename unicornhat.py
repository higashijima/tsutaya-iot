import datetime
from PIL import Image, ImageDraw, ImageFont
import unicornhathd as hat
import time

DEFAULT_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

class unicorn:
  def __init__(self, font=DEFAULT_FONT, cycle=0.1):
    self.width, self.height = hat.get_shape()
    self.font = ImageFont.truetype(font, 9)
    self.cycle = cycle
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

  # アイコン表示
  def disp_icon(iconpath):
    image = Image.open(iconpath)
    for ox in range(int(image.size[0]/self.width)):
      for oy in range(int(image.size[1]/self.height)):
        valid = False
        for x in range(self.width):
          for y in range(self.height):
            pixel = image.getpixel(((ox*width)+y, (oy*height)+x))
            r, g, b = int(pixel), int(pixel[1]), int(pixel[2])
            if r or g or b:
              valid = True
            hat.set_pixecl(x, y, r, g, b)
        if valid:
          hat.show()
          time.sleep(self.cycle)
    

if __name__=='__main__':
  u = unicorn()
  u.disp_clock((0, 220, 220))
  time.sleep(0.5)
  u.disp_icon('./icon/us.png') 
  time.sleep(0.5)
  u.disp_icon('./icon/weather/cloud.png')
