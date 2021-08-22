import time
import board
import displayio
from simpleio import map_range
from normal_screen import NormalScreen
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect


class BigScreen(NormalScreen):

    def __init__(self, sensors, battery, update_frequency=5*60):
        self._aqi_label = None
        self._aqi = ""
        super().__init__(sensors, battery, update_frequency)

    def refresh(self):
        need_refresh = False
        need_refresh += self.update_temperature()
        need_refresh += self.update_humidity()
        need_refresh += self.update_pressure()
        need_refresh += self.update_aqi()
        need_refresh += self.update_battery_pourcentage()
        need_refresh += self.update_battery_level()
        need_refresh += self.update_display_mode()
        self._batt_label.hidden = not self.show_battery_value
        return need_refresh

    def update_aqi(self):
        val, tier = self.calculate_pm25_aqi()
        new_aqi = "{0}".format(int(val))
        if new_aqi == self._aqi:
            return False
        self._aqi = new_aqi
        self._aqi_label.text = self._aqi
        return True

    def calculate_pm25_aqi(self):
        aqi_val = 0
        aqi_cat = ""
        # Check sensor reading using EPA breakpoint (Clow-Chigh)
        if 0.0 <= self._sensors.environmental_pm25_stats.mean <= 12.0:
            # AQI calculation using EPA breakpoints (Ilow-IHigh)
            aqi_val = map_range(int(self._sensors.environmental_pm25_stats.mean), 0, 12, 0, 50)
            aqi_cat = "Good"
        elif 12.1 <= self._sensors.environmental_pm25_stats.mean <= 35.4:
            aqi_val = map_range(int(self._sensors.environmental_pm25_stats.mean), 12, 35, 51, 100)
            aqi_cat = "Moderate"
        elif 35.5 <= self._sensors.environmental_pm25_stats.mean <= 55.4:
            aqi_val = map_range(int(self._sensors.environmental_pm25_stats.mean), 36, 55, 101, 150)
            aqi_cat = "Unhealthy for Sensitive Groups"
        elif 55.5 <= self._sensors.environmental_pm25_stats.mean <= 150.4:
            aqi_val = map_range(int(self._sensors.environmental_pm25_stats.mean), 56, 150, 151, 200)
            aqi_cat = "Unhealthy"
        elif 150.5 <= self._sensors.environmental_pm25_stats.mean <= 250.4:
            aqi_val = map_range(int(self._sensors.environmental_pm25_stats.mean), 151, 250, 201, 300)
            aqi_cat = "Very Unhealthy"
        elif 250.5 <= self._sensors.environmental_pm25_stats.mean <= 350.4:
            aqi_val = map_range(int(self._sensors.environmental_pm25_stats.mean), 251, 350, 301, 400)
            aqi_cat = "Hazardous"
        elif 350.5 <= self._sensors.environmental_pm25_stats.mean <= 500.4:
            aqi_val = map_range(int(self._sensors.environmental_pm25_stats.mean), 351, 500, 401, 500)
            aqi_cat = "Hazardous"
        return aqi_val, aqi_cat

    def setup_screen(self):
        self._display = board.DISPLAY

        self._group = displayio.Group(max_size=20)

        # background
        rect1 = Rect(0, 0, 199, 90, fill=0xFFFFFF)
        rect2 = Rect(200, 0, 296, 90, fill=0xBBBBBB)
        rect3 = Rect(0, 91, 296, 128, fill=0x444444)

        # Create fonts
        print("BigScreen - Loading fonts")
        big_font = bitmap_font.load_font("/Exo-Bold-42.bdf")
        medium_font = bitmap_font.load_font("/Exo-SemiBold-18.bdf")
        small_font = bitmap_font.load_font("/Exo-SemiBold-12.bdf")
        tiny_font = bitmap_font.load_font("/Exo-SemiBold-6.bdf")

        ## Bitmaps
        print("BigScreen - Loading bitmaps")
        thermometer_bitmap = displayio.OnDiskBitmap(open("/thermometer.bmp", "rb"))
        temperature_tile = displayio.TileGrid(thermometer_bitmap, pixel_shader=displayio.ColorConverter(), x=4, y=18)
        humidity_bitmap = displayio.OnDiskBitmap(open("/water.bmp", "rb"))
        humidity_tile = displayio.TileGrid(humidity_bitmap, pixel_shader=displayio.ColorConverter(), x=3, y=100)
        pressure_bitmap = displayio.OnDiskBitmap(open("/cloud.bmp", "rb"))
        pressure_tile = displayio.TileGrid(pressure_bitmap, pixel_shader=displayio.ColorConverter(), x=120, y=100)

        # Create sensor value labels
        print("BigScreen - Create sensors labels")
        self._temperature_label = label.Label(big_font, text="012.45°", color=0x000000, x=28, y=45, background_color=0xFFFFFF)
        self._temperature_label.anchor_point = (0.5, 0.5)
        self._temperature_label.anchored_position = (100, 45)
        self._humidity_label = label.Label(medium_font, text="012.34%", color=0xFFFFFF, x=24, y=110, background_color=0x444444)
        self._pressure_label = label.Label(medium_font, text="1234hPa", color=0xFFFFFF, x=150, y=110, background_color=0x444444)
        aqi_text = label.Label(medium_font, text="AQI", color=0x000000, x=218, y=8, background_color=0xBBBBBB)
        aqi_text.anchor_point = (0.5, 0)
        aqi_text.anchored_position = (245, 8)
        self._aqi_label = label.Label(medium_font, text="1234", color=0x000000, x=218, y=50, background_color=0xBBBBBB)
        self._aqi_label.anchor_point = (0.5, 0)
        self._aqi_label.anchored_position = (245, 50)

        # Create battery level graphic
        print("BigScreen - Create battery level graphic")
        battery_anode = Rect(1, 3, 2, 8, fill=0xFFFFFF, outline=0x000000, stroke=2)
        battery_body = RoundRect(3, 1, 24, 12, 2,  outline=0x000000, stroke=2)
        self._batt_label = label.Label(tiny_font, text="1234", color=0x000000, x=30, y=4, background_color=0xBBBBBB)
        self._batt_label.anchor_point = (0, 0)
        self._batt_label.anchored_position = (30, 4)

        self._battery_level100 = Rect(4, 2, 22, 10, fill=0x444444)
        self._battery_level75 = Rect(4, 2, int(22*0.75), 10, fill=0x444444)
        self._battery_level50 = Rect(4, 2, int(22*0.50), 10, fill=0x444444)
        self._battery_level25 = Rect(4, 2, int(22*0.25), 10, fill=0x444444)
        self.hide_all_battery_level()

        # Display data mode
        self._mode_label = label.Label(tiny_font, text="Curr", color=0x000000, x=150, y=4, background_color=0xBBBBBB)
        self._mode_label.anchor_point = (0, 0)
        self._mode_label.anchored_position = (150, 4)

        # Compose group
        print("BigScreen - Compose group")
        self._group.append(rect1)
        self._group.append(rect2)
        self._group.append(rect3)
        self._group.append(self._battery_level100)
        self._group.append(self._battery_level75)
        self._group.append(self._battery_level50)
        self._group.append(self._battery_level25)
        self._group.append(battery_anode)
        self._group.append(battery_body)
        self._group.append(self._temperature_label)
        self._group.append(self._humidity_label)
        self._group.append(self._pressure_label)
        self._group.append(aqi_text)
        self._group.append(self._aqi_label)
        self._group.append(self._batt_label)
        self._group.append(self._mode_label)
        self._group.append(temperature_tile)
        self._group.append(humidity_tile)
        self._group.append(pressure_tile)
        print("BigScreen - Finish setup")
