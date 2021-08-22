import time
import board
import displayio
from screen import Screen, DisplayDataMode
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect


class NormalScreen(Screen):

    def __init__(self, sensors, battery, update_frequency=5*60):
        self._temperature_label = None
        self._humidity_label = None
        self._pressure_label = None
        self._battery_level100 = None
        self._battery_level75 = None
        self._battery_level50 = None
        self._battery_level25 = None
        self._batt_label = None
        self._mode_label = None
        self._temperature = ""
        self._humidity = ""
        self._pressure = ""
        self._battery_level = ""
        self._battery_pourcentage = 100
        self._display_mode = ""
        super().__init__(sensors, battery, update_frequency)

    @property
    def temperature(self):
        if self._display_data_mode == DisplayDataMode.Current:
            return self._sensors.temperature
        elif self._display_data_mode == DisplayDataMode.Min:
            return self._sensors.temperature_stats.min
        elif self._display_data_mode == DisplayDataMode.Max:
            return self._sensors.temperature_stats.max
        elif self._display_data_mode == DisplayDataMode.Average:
            return self._sensors.temperature_stats.mean

    @property
    def humidity(self):
        if self._display_data_mode == DisplayDataMode.Current:
            return self._sensors.humidity
        elif self._display_data_mode == DisplayDataMode.Min:
            return self._sensors.humidity_stats.min
        elif self._display_data_mode == DisplayDataMode.Max:
            return self._sensors.humidity_stats.max
        elif self._display_data_mode == DisplayDataMode.Average:
            return self._sensors.humidity_stats.mean

    @property
    def pressure(self):
        if self._display_data_mode == DisplayDataMode.Current:
            return self._sensors.pressure
        elif self._display_data_mode == DisplayDataMode.Min:
            return self._sensors.pressure_stats.min
        elif self._display_data_mode == DisplayDataMode.Max:
            return self._sensors.pressure_stats.max
        elif self._display_data_mode == DisplayDataMode.Average:
            return self._sensors.pressure_stats.mean

    def refresh(self):
        need_refresh = False
        need_refresh += self.update_temperature()
        need_refresh += self.update_humidity()
        need_refresh += self.update_pressure()
        need_refresh += self.update_battery_pourcentage()
        need_refresh += self.update_battery_level()
        need_refresh += self.update_display_mode()
        self._batt_label.hidden = not self.show_battery_value
        print("NormalScreen - refresh", need_refresh)
        return need_refresh

    def update_temperature(self):
        new_temperature = "{:4.1f}°".format(self.temperature)
        if new_temperature == self._temperature:
            return False
        self._temperature = new_temperature
        self._temperature_label.text = self._temperature
        return True

    def update_humidity(self):
        new_humidity = "{:4.1f}%".format(self.humidity)
        if new_humidity == self._humidity:
            return False
        self._humidity = new_humidity
        self._humidity_label.text = self._humidity
        return True

    def update_pressure(self):
        new_pressure = "{:4.0f} hPa".format(self.pressure)
        if new_pressure == self._pressure:
            return False
        self._pressure = new_pressure
        self._pressure_label.text = self._pressure
        return True

    def update_battery_level(self):
        new_battery_level = "{:1.1f}v".format(self._battery.level)
        if new_battery_level == self._battery_level:
            return False
        self._battery_level = new_battery_level
        self._batt_label.text = self._battery_level
        return True

    def update_battery_pourcentage(self):
        new_battery_pourcentage = self._battery.pourcentage
        if new_battery_pourcentage == self._battery_pourcentage:
            return False
        self.hide_all_battery_level()
        if new_battery_pourcentage > 75:
            self._battery_level100.hidden = False
        elif new_battery_pourcentage > 50:
            self._battery_level75.hidden = False
        elif new_battery_pourcentage > 25:
            self._battery_level50.hidden = False
        elif new_battery_pourcentage > 5:
            self._battery_level25.hidden = False

        self._battery_pourcentage = new_battery_pourcentage
        return True

    def hide_all_battery_level(self):
        self._battery_level100.hidden = True
        self._battery_level75.hidden = True
        self._battery_level50.hidden = True
        self._battery_level25.hidden = True

    def update_display_mode(self):
        new_display_mode = self.display_data_mode_str
        if new_display_mode == self._display_mode:
            return False
        self._display_mode = new_display_mode
        self._mode_label.text = self._display_mode
        return True

    def setup_screen(self):
        self._display = board.DISPLAY

        self._group = displayio.Group(max_size=20)

        # background
        rect1 = Rect(0, 0, 296, 90, fill=0xFFFFFF)
        rect3 = Rect(0, 91, 296, 128, fill=0x444444)

        # Create fonts
        print("NormalScreen - Loading fonts")
        big_font = bitmap_font.load_font("/Exo-Bold-42.bdf")
        medium_font = bitmap_font.load_font("/Exo-SemiBold-18.bdf")
        small_font = bitmap_font.load_font("/Exo-SemiBold-12.bdf")
        tiny_font = bitmap_font.load_font("/Exo-SemiBold-6.bdf")

        ## Bitmaps
        print("NormalScreen - Loading bitmaps")
        thermometer_bitmap = displayio.OnDiskBitmap(open("/thermometer.bmp", "rb"))
        temperature_tile = displayio.TileGrid(thermometer_bitmap, pixel_shader=displayio.ColorConverter(), x=4, y=18)
        humidity_bitmap = displayio.OnDiskBitmap(open("/water.bmp", "rb"))
        humidity_tile = displayio.TileGrid(humidity_bitmap, pixel_shader=displayio.ColorConverter(), x=3, y=100)
        pressure_bitmap = displayio.OnDiskBitmap(open("/cloud.bmp", "rb"))
        pressure_tile = displayio.TileGrid(pressure_bitmap, pixel_shader=displayio.ColorConverter(), x=120, y=100)

        # Create sensor value labels
        print("NormalScreen - Create sensors labels")
        self._temperature_label = label.Label(big_font, text="012.45°", color=0x000000, x=28, y=45, background_color=0xFFFFFF)
        self._temperature_label.anchor_point = (0.5, 0.5)
        self._temperature_label.anchored_position = (100, 45)
        self._humidity_label = label.Label(medium_font, text="012.34%", color=0xFFFFFF, x=24, y=110, background_color=0x444444)
        self._pressure_label = label.Label(medium_font, text="1234hPa", color=0xFFFFFF, x=150, y=110, background_color=0x444444)

        # Create battery level graphic
        print("NormalScreen - Create battery level graphic")
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
        print("NormalScreen - Compose group")
        self._group.append(rect1)
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
        self._group.append(self._batt_label)
        self._group.append(self._mode_label)
        self._group.append(temperature_tile)
        self._group.append(humidity_tile)
        self._group.append(pressure_tile)
        print("NormalScreen - Finish setup")
