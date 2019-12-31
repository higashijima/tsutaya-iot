import sys
import time

from envirophat import light, weather, motion, analog

class enviro:
  def __init__(self, unit):
    self.unit = unit

  def getJsonDatas(self):
    a = weather.altitude()
    t = weather.temperature()
    p = weather.pressure(unit=self.unit)

    return '{{"altitude": {0:.2f}, "templature": {0:.2f}, "pressure": {0:.2f}}}'.format(a, t, p)

if __name__ == '__main__':
  e = enviro('hPa')
  d = e.getJsonDatas()
  print(d)

