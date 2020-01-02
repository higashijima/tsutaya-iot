import sys
import time

from envirophat import light, weather, motion, analog

class enviro:
  def getJsonDatas():
    a = weather.altitude()
    t = weather.templature()
    p = weather.pressure(unit='hPa')

    return '"altitude": {a:.2f}, "templature": {t:.2f}, "pressure": {p:.2f}'.format(a, t, p)

if __name__ == '__main__':
  e = enviro()
  d = e.getJsonData()
  print(d)

