from button import Button

class Buttons(object):

    def __init__(self, magtag):
        self._magtag = magtag
        self._button_a = Button(self._magtag.peripherals.buttons[0], "A")
        self._button_b = Button(self._magtag.peripherals.buttons[1], "B")
        self._button_c = Button(self._magtag.peripherals.buttons[2], "C")
        self._button_d = Button(self._magtag.peripherals.buttons[3], "D")

    @property
    def button_a(self):
        return self._button_a

    @property
    def button_b(self):
        return self._button_b

    @property
    def button_c(self):
        return self._button_c

    @property
    def button_d(self):
        return self._button_d

    def update(self):
        self._button_a.update()
        self._button_b.update()
        self._button_c.update()
        self._button_d.update()
