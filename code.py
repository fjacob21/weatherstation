# Magtag Slideshow
# auto plays .bmp images in /slides folder
# press left and right buttons to go back or forward one slide
# press down button to toggle autoplay mode
# press up button to toggle sound

import time
import terminalio
from adafruit_magtag.magtag import MagTag
from sensors import Sensors
from battery import Battery
from buttons import Buttons
from lighting import Lighting
from big_screen import BigScreen
from fatal_screen import FatalScreen
from normal_screen import NormalScreen
import displayio
from rtc import RTC
from adafruit_magtag.magtag import Graphics
from adafruit_magtag.magtag import Network
from adafruit_magtag.magtag import Peripherals
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label

CYCLE_TIME = 0.01

class DeviceType(object):
    Invalid = 0
    Normal = 1
    Big = 2


magtag = MagTag()
sensors = Sensors()
battery = Battery(magtag)
buttons = Buttons(magtag)
lighting = Lighting(magtag)

if sensors.no_sensors:
    print("No sensors present!!!!")
    device_type = DeviceType.Invalid
    screen = FatalScreen(sensors, battery)
elif sensors.pm25_present and sensors.bme680_present:
    print("Big device type")
    device_type = DeviceType.Big
    screen = BigScreen(sensors, battery)
else:
    print("Normal device type")
    device_type = DeviceType.Normal
    screen = NormalScreen(sensors, battery)

screen.update(True)

while True:
    screen.update()
    sensors.update()
    lighting.update()
    buttons.update()
    if buttons.button_a.is_button_down_event:
        lighting.blink(Lighting.WHITE, 10)

    if buttons.button_b.is_button_down_event:
        screen.toggle_display_data_mode()

    if buttons.button_d.is_button_down_event:
        screen.show_battery_value = not screen.show_battery_value

    time.sleep(CYCLE_TIME)
