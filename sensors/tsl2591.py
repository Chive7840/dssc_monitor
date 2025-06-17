import board
import busio
import adafruit_tsl2591

class TSL2591Sensor:
    """
    Interface for the Adafruit TSL2591 High Dynamic Range Digital Light Sensor.
    """
    
    def __init__(self) -> None:
        """
        Initializes the I2C connection and sensor instance.
        """
        
        try:            
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_tsl2591.TSL2591(i2c)
        except RuntimeError as err:
            raise ConnectionError(f"[ERROR] Failed to initialize TSL2591 sensor over I2C: {err}") from err
        
    def read_lux(self) -> float:
        """
        Reads the current ambient light level in lux.
        
        Returns:
            float: Light level in lux.
        """
        return self.sensor.lux