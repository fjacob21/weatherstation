import board
import busio
import time
from adafruit_pm25.i2c import PM25_I2C
import adafruit_bme680
from running_stats import RunningStats


class Sensors(object):

    INVALID_TEMPERATURE = -200
    INVALID_HUMIDITY = -100
    INVALID_PRESSURE = -300
    INVALID_ALTITUDE = -400
    INVALID_GAS = -500
    INVALID_PM25 = -600

    def __init__(self, temperature_offset=-1, sea_level_pressure=1013.25):
        self._i2c = None
        self._pm25 = None
        self._bme680 = None
        self._temperature_offset = temperature_offset
        self._sea_level_pressure = sea_level_pressure
        self._pm25_data = None
        self._last_update = 0.0
        self._update_frequency = 1.0
        self._temperature_stats = RunningStats()
        self._humidity_stats = RunningStats()
        self._pressure_stats = RunningStats()
        self._environmental_pm25_stats = RunningStats()
        self.init()

    @property
    def pm25_present(self):
        return self._pm25 is not None

    @property
    def bme680_present(self):
        return self._bme680 is not None

    @property
    def no_sensors(self):
        return not self.bme680_present and not self.pm25_present

    @property
    def temperature(self):
        if not self.bme680_present:
            return Sensors.INVALID_TEMPERATURE
        return self._bme680.temperature + self._temperature_offset

    @property
    def humidity(self):
        if not self.bme680_present:
            return Sensors.INVALID_HUMIDITY
        return self._bme680.humidity

    @property
    def pressure(self):
        if not self.bme680_present:
            return Sensors.INVALID_PRESSURE
        return self._bme680.pressure

    @property
    def altitude(self):
        if not self.bme680_present:
            return Sensors.INVALID_ALTITUDE
        return self._bme680.altitude

    @property
    def gas(self):
        if not self.bme680_present:
            return Sensors.INVALID_GAS
        return self._bme680.gas

    @property
    def environmental_pm10(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm10_data["pm25 env"]

    @property
    def environmental_pm25(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["pm25 env"]

    @property
    def environmental_pm100(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["pm100 env"]

    @property
    def standard_pm10(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["pm10 standard"]

    @property
    def standard_pm25(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["pm25 standard"]

    @property
    def standard_pm100(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["pm100 standard"]

    @property
    def particule_03(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["particles 03um"]

    @property
    def particule_10(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["particles 10um"]

    @property
    def particule_25(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["particles 25um"]

    @property
    def particule_50(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["particles 50um"]

    @property
    def particule_100(self):
        if not self.pm25_present:
            return Sensors.INVALID_PM25
        return self._pm25_data["particles 100um"]

    @property
    def temperature_stats(self):
        return self._temperature_stats

    @property
    def humidity_stats(self):
        return self._humidity_stats

    @property
    def pressure_stats(self):
        return self._pressure_stats

    @property
    def environmental_pm25_stats(self):
        return self._environmental_pm25_stats

    def init(self):
        self.init_i2c()
        self.init_bme680()
        self.init_pm25()
        self.update(True)

    def init_i2c(self):
        # Create library object, use 'slow' 100KHz frequency!
        self._i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

    def init_pm25(self):
        try:
            # Connect to a PM2.5 sensor over I2C
            self._pm25 = PM25_I2C(self._i2c, None)
        except Exception:
            print("PM2.5 sensor not present")

    def init_bme680(self):
        try:
            self._bme680 = adafruit_bme680.Adafruit_BME680_I2C(self._i2c)
            self._bme680.sea_level_pressure = self._sea_level_pressure
        except Exception:
            print("BME680 sensor not present")

    def update(self, force=False):
        if force or (time.monotonic() - self._last_update >= self._update_frequency):
            try:
                self._pm25_data = self._pm25.read()
                self._temperature_stats.add(self.temperature)
                self._humidity_stats.add(self.humidity)
                self._pressure_stats.add(self.pressure)
                self._environmental_pm25_stats.add(self.environmental_pm25)
                self._last_update = time.monotonic()
            except Exception as e:
                print(e)
