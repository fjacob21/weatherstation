

class Button(object):

    def __init__(self, button, name=""):
        self._button = button
        self._name = name
        self._value = self._button.value
        self._button_up_event = False
        self._button_down_event = False

    @property
    def is_button_pressed(self):
        return self._value

    @property
    def is_button_down_event(self):
        event = self._button_down_event
        self._button_down_event = False
        return event

    @property
    def is_button_up_event(self):
        event = self._button_up_event
        self._button_up_event = False
        return event

    def update(self):
        new_value = self._button.value
        if new_value != self._value:
            self._value = new_value
            if new_value:
                print("Button {0} up event".format(self._name))
                self._button_up_event = True
            else:
                print("Button {0} down event".format(self._name))
                self._button_down_event = True
