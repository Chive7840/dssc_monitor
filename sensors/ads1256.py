import spidev

class ADS1256:
    def __init__(self, vref=2.5, channel=0):
        self.vref = vref
        self.channel=channel
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)     # SPI0 CE0
        self.spi.max_speed_hz = 1000000

    def read_raw(self):
        # Dummy raw value initially (replace with actual ADS1256 read code)
        return 500000

    def read_voltage(self):
        raw = self.read_raw()
        voltage = (raw/ 0x7FFFFF) * self.vref
        return voltage