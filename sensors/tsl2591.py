import board
import busio
import adafruit_tsl2591
from adafruit_tsl2591 import TSL2591

class TSL2591Sensor:
    """
    Interface for the Adafruit TSL2591 High Dynamic Range Digital Light Sensor.
    """
    GAIN_LOW = adafruit_tsl2591.GAIN_LOW
    GAIN_MED = adafruit_tsl2591.GAIN_MED
    GAIN_HIGH = adafruit_tsl2591.GAIN_HIGH
    GAIN_MAX = adafruit_tsl2591.GAIN_MAX
    
    INTEGRATIONTIME_100MS = adafruit_tsl2591.INTEGRATIONTIME_100MS
    INTEGRATIONTIME_200MS = adafruit_tsl2591.INTEGRATIONTIME_200MS
    INTEGRATIONTIME_300MS = adafruit_tsl2591.INTEGRATIONTIME_300MS
    INTEGRATIONTIME_400MS = adafruit_tsl2591.INTEGRATIONTIME_400MS
    INTEGRATIONTIME_500MS = adafruit_tsl2591.INTEGRATIONTIME_500MS
    INTEGRATIONTIME_600MS = adafruit_tsl2591.INTEGRATIONTIME_600MS
    
    
    def __init__(self) -> None:
        """
        Initializes the I2C connection and sensor instance.
        """
        
        try:            
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = TSL2591(i2c)
        except RuntimeError as err:
            raise ConnectionError(f"[ERROR] Failed to initialize TSL2591 sensor over I2C: {err}") from err
        
    def read_lux(self, retry_on_overflow: bool = True) -> float:
        """
        Reads the current ambient light level in lux.
        
        Returns:
            float: Light level in lux, or 0.0 if overflow error occurs.
        """
        try:
            return self.sensor.lux
        except OverflowError:
            print(f"[TSL2591] OverflowError: Saturation reached. Consider reducing gain.")
            if retry_on_overflow:
                self.set_gain(self.GAIN_LOW)
                self.set_integration_time(self.INTEGRATIONTIME_100MS)
                sleep(0.1) # Gives sensor time to apply new settings
                try:
                    return self.sensor.lux
                except OverflowError:
                    print("[TSL2591] Overflow persisted after gain/integration adjustment.")
            return 0.0
     
    def read_raw_channels(self) -> tuple[int, int]:
        """
        Returns raw channel values:  (full spectrum, infrared)
        """
        return self.sensor.raw_luminosity
    
    # ----------------------------------------------------------------
    # GAIN CONTROL
    # ----------------------------------------------------------------
    def get_gain(self) -> int:
        """
        Returns the current gain setting.
        """
        return self.sensor.gain
    
    def set_gain(self, gain: int) -> None:
        """
        Sets the gain level of the sensor.
        
        Args:
            gain (int): One of GAIN_LOW, GAIN_MED, GAIN_HIGH, GAIN_MAX.
            
        Raises:
            ValueError: If the provided gain is not a valid setting.
        """
        valid_gains = {
            self.GAIN_LOW,
            self.GAIN_MED,
            self.GAIN_HIGH,
            self.GAIN_MAX
        }
        
        if gain not in valid_gains:
            raise ValueError("Invalid gain setting.")
        
        self.sensor.gain = gain
        
    # ----------------------------------------------------------------
    # INTEGRATION TIME CONTROL
    # ----------------------------------------------------------------
    def get_integration_time(self) -> int:
        """
        Returns the current integration time setting.
        """
        return self.sensor.integration_time
    
    def set_integration_time(self, integration_time: int) -> None:
        """
        Sets the integration time of the sensor.
        
        Args:
            integration_time (int): One of INTEGRATIONTIME_100MS, INTEGRATIONTIME_200MS,
                                            INTEGRATIONTIME_300MS, INTEGRATIONTIME_400MS,
                                            INTEGRATIONTIME_500MS, INTEGRATIONTIME_600MS.
                                            
        Raises:
            ValueError: If the provided integration_time is not a valid setting.
        """
        valid_integration_times = {
            self.INTEGRATIONTIME_100MS,
            self.INTEGRATIONTIME_200MS,
            self.INTEGRATIONTIME_300MS,
            self.INTEGRATIONTIME_400MS,
            self.INTEGRATIONTIME_500MS,
            self.INTEGRATIONTIME_600MS,
        }
        
        if integration_time not in valid_integration_times:
            raise ValueError("Invalid integration time setting.")
        self.sensor.integration_time = integration_time
        
