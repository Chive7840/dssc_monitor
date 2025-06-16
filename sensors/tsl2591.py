from .waveshare_TSL2591.TSL2591 import TSL2591
import board
import busio
import adafruit_tsl2591

class TSL2591Sensor:
    def __init__(self):
        #self.sensor = TSL2591()
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_tsl2591.TSL2591(i2c)
        
    def read_lux(self) -> float:
        #return self.sensor.Lux
        return self.sensor.lux