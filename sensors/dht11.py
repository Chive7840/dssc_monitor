import board
import adafruit_dht
from typing import Optional, Tuple
from time import sleep

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
        
    def read(self, retries: int = 5, delay: float = 2.0) -> Optional[Tuple[float, float]]:
        """
        Attempts to read temperature and humidity values from the sensor.
        
        Args:
            retries (int): Number of times to retry reading on failure.
            delay (float): Seconds to wait between retries.
        
        Returns:
            Optional[Tuple[float, float]]: (temperature, humidity) or None if all attempts fail.
        """
        for attempt in range(retries):
            try:        
                temperature = self.sensor.temperature	# °C
                humidity = self.sensor.humidity			# %
                
                if temperature is not None and humidity is not None:
                    return temperature, humidity
            except (RuntimeError, ValueError) as err:
                print(f"[DHT11Sensor] Read error on attempt {attempt + 1}: {err}")
                sleep(delay)
        
        print(f"[DHT11Sensor] All read attempts failed.")
        return None
        
    def cleanup(self) -> None:
        """
        Frees sensor resources. Useful for GPIO cleanup in long-running applications.
        """
        try:
            self.sensor.exit()
        except Exception as err:
            print(f"[DHT11Sensor] Cleanup warning: {err}")