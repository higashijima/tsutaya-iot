import datetime
from PIL import Image, ImageDraw, ImageFont
import unicornhathd as hat
import time

DEFAULT_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
class unicorn:
  def __init__(self, font=DEFAULT_FONT):
    self.width, self.height = hat.get_shape()
    self.font = ImageFont.truetype(font, 9)
    hat.rotation(0)

  # ディスプレイクリア
  def init_disp(self, image):
    image = Image.new("RGB", (self.width, self.height), (0, 0, 0))
    draw = ImageDraw(image)
    return image

  # ディスプレイ表示
  def draw_disp(self, image):
    for x in range(self.width):
      for y in range(self.height):
        r, g, b = image.getpixel((x, y))
        hat.set_pixel(self.width-x-1, y, r, g, b)
    hat.show()


  # 時刻表示
  def disp_clock():
    now = datetime.datetime.now()
    image = init_disp(image)
    draw.text((0, -1), '{0:02}'.format(now.hour), fill=self.color, font=self.font)
    draw.text((0, 8), '{0:02}'.format(now.minute), fill=self.color, font=self.font)
    hat.clear()

    draw_disp(image)
    
