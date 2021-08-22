import time
import board
import displayio
from screen import Screen
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect


class FatalScreen(Screen):

    def __init__(self, sensors, battery, update_frequency=5*60):
        super().__init__(sensors, battery, update_frequency)

    def setup_screen(self):
        self._display = board.DISPLAY

        self._group = displayio.Group(max_size=20)

        # background
        rect1 = Rect(0, 0, 296, 128, fill=0xFFFFFF)

        # Create fonts
        print("FatalScreen - Loading fonts")
        medium_font = bitmap_font.load_font("/Exo-SemiBold-18.bdf")

        # Create sensor value labels
        print("FatalScreen - Create sensors labels")
        self._error_label = label.Label(medium_font, text="Fatal Error no sensors!!!°", color=0x000000, x=28, y=45, background_color=0xFFFFFF)
        self._error_label.anchor_point = (0.5, 0.5)
        self._error_label.anchored_position = (100, 45)

        # Compose group
        print("FatalScreen - Compose group")
        self._group.append(rect1)
        self._group.append(self._error_label)
        print("FatalScreen - Finish setup")
