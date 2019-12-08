from unicornhat import unicorn
import unicornhathd as hat
import time

u = unicorn()
u.disp_clock((0, 220, 220))
time.sleep(0.5)
u.disp_icon('./icons/us.png') 
time.sleep(2)
u.disp_icon('./icons/weather/cloudy.png')
time.sleep(1)
image, draw = u.init_disp()
u.disp_text(draw, (0,-1), '1023mb', (255,255,0))
u.disp_text(draw, (0,8), '23C', (255,0,240))

hat.clear()
u.draw_disp(image)

