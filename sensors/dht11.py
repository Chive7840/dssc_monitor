import board
import adafruit_dht
from typing import Optional, Tuple

class DHT11Sensor:
    """
    Handles interaction with a DHT11 temperature/humidity sensor.
    """
    
    
    def __init__(self, pin=board.D17):
        """
        Initializes the DHT11 sensor on the specified GPIO pin.
        
        Args:
            pin: The GPIO pin the DHT11 is connected to (default is board.D17).
        """
        self.sensor = adafruit_dht.DHT11(pin)
        
    def read(self) -> Optional[Tuple[float, float]]:
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
        except (RuntimeError, ValueError) as err:
            print(f"[DHT11Sensor] Read error: {err}")
            return None
        
    def cleanup(self) -> None:
        """
        Frees sensor resources. Useful for GPIO cleanup in long-running applications.
        """
        self.sensor.exit()