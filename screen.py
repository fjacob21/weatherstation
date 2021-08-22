import time
import displayio


class DisplayDataMode(object):
    Current = 0
    Max = 1
    Min = 2
    Average = 3


class Screen(object):

    def __init__(self, sensors, battery, update_frequency=5*60, show_battery_value=False):
        print("Screen - Init")
        self._sensors = sensors
        self._battery = battery
        self._show_battery_value = show_battery_value
        self._display_data_mode = DisplayDataMode.Current
        self._display = None
        self._group = None
        self._last_update = 0.0
        self._force_update = False
        self._update_frequency = float(update_frequency)
        self._minimal_update_frequency = 10.0
        self.setup_screen()

    @property
    def show_battery_value(self):
        return self._show_battery_value

    @show_battery_value.setter
    def show_battery_value(self, value):
        self._show_battery_value = value
        self._force_update = True

    @property
    def display_data_mode_str(self):
        if self._display_data_mode == DisplayDataMode.Current:
            return "Curr"
        elif self._display_data_mode == DisplayDataMode.Min:
            return "Min"
        elif self._display_data_mode == DisplayDataMode.Max:
            return "Max"
        elif self._display_data_mode == DisplayDataMode.Average:
            return "Avg"

    def toggle_display_data_mode(self):
        if self._display_data_mode == DisplayDataMode.Current:
            self._display_data_mode = DisplayDataMode.Min
            print("Switching to min")
        elif self._display_data_mode == DisplayDataMode.Min:
            self._display_data_mode = DisplayDataMode.Max
            print("Switching to mac")
        elif self._display_data_mode == DisplayDataMode.Max:
            self._display_data_mode = DisplayDataMode.Average
            print("Switching to avg")
        elif self._display_data_mode == DisplayDataMode.Average:
            self._display_data_mode = DisplayDataMode.Current
            print("Switching to curr")
        self._force_update = True


    def setup_screen(self):
        self._display = board.DISPLAY
        self._group = displayio.Group(max_size=20)
        print("Screen - Finish setup")

    def update(self, force=False):
        if (
            force
            or (self._force_update and time.monotonic() - self._last_update >= self._minimal_update_frequency)
            or (time.monotonic() - self._last_update >= self._update_frequency)):
            if self.refresh() or force:
                try:
                    print("Screen - Update")
                    self._force_update = False
                    self._display.show(self._group)
                    self._display.refresh()
                except Exception as e:
                    print(e)
            self._last_update = time.monotonic()

    def refresh(self):
        return
