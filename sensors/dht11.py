import board
import adafruit_dht

class DHT11Sensor:
    def __init__(self, pin=board.D17):
        self.sensor = adafruit_dht.DHT11(pin)
        
    def read(self) -> tuple[float, float]:
        temperature = self.sensor.temperature	# °C
        humidity = self.sensor.humidity			# %
        
        return temperature, humidity
