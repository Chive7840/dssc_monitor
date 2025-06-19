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
        
    def read_lux(self) -> float:
        """
        Reads the current ambient light level in lux.
        
        Returns:
            float: Light level in lux.
        """
        return self.sensor.lux
    
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
        
    # ----------------------------------------------------------------
    # AUTOMATIC GAIN ADJUSTMENT
    # ----------------------------------------------------------------   
    def auto_gain_adjust(self) -> None:
        """
        Automatically adjusts sensor gain and integration time based on the current lux value.
        This improves accuracy in varying light conditions without requiring user input.
        """
        try:
            full, ir = self.read_raw_channels()
            total = full + ir
        except RuntimeError as err:
            print(f"[TSL2591] Failed to read raw channels: {err}")
            return
        
        gain = self.get_gain()
        integration = self.get_integration_time()
        
        # Definitions for adjustment thresholds
        if total < 100:
            desired_gain = self.GAIN_MAX
            desired_time = self.INTEGRATIONTIME_600MS
        elif total < 1000:
            desired_gain = self.GAIN_HIGH
            desired_time = self.INTEGRATIONTIME_400MS
        elif total < 8000:
            desired_gain = self.GAIN_MED
            desired_time = self.INTEGRATIONTIME_300MS
        elif total < 30000:
            desired_gain = self.GAIN_LOW
            desired_time = self.INTEGRATIONTIME_200MS
        else:
            desired_gain = self.GAIN_LOW
            desired_time = self.INTEGRATIONTIME_100MS
            
        # Check if the current values need to be adjusted
        changed = False
        if gain != desired_gain:
            self.set_gain(desired_gain)
            changed = True
            
        if integration != desired_time:
            self.set_integration_time(desired_time)
            changed = True
            
        if changed:
            print(f"[TSL2591] Auto-adjusted: gain set to {gain},"
                  f"integration time set to {integration}")