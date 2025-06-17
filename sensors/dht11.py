import board
import adafruit_dht

class DHT11Sensor:
    """
    Handles interaction with a DHT11 temperature/humidity sensor.
    """
    
    
    def __init__(self, pin=board.D17):
        self.sensor = adafruit_dht.DHT11(pin)
        
    def read(self) -> tuple[float | None, float | None]:
        """
        Attempts to read temperature and humidity values from the sensor.
        
        Returns:
            A tuple containing (temperature in °C, himdity in %),
            or (None, None) if reading fails.
        """
        try:        
            temperature = self.sensor.temperature	# °C
            humidity = self.sensor.humidity			# %
            return temperature, humidity
        except RuntimeError:
            # DHT sensors occasionally return errors. Retry logic can be added if needed.
            return None, None
        
    def cleanup(self) -> None:
        """
        Frees sensor resources. Useful for GPIO cleanup in long-running applications.
        """
        self.sensor.exit()