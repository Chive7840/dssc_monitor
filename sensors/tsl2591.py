import board
import busio
import adafruit_tsl2591
from adafruit_tsl2591 import (
    TSL2591, GAIN_LOW, GAIN_MED, GAIN_HIGH, GAIN_MAX,
    INTEGRATIONTIME_100MS, INTEGRATIONTIME_200MS, INTEGRATIONTIME_300MS,
    INTEGRATIONTIME_400MS, INTEGRATIONTIME_500MS, INTEGRATIONTIME_600MS,
)

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
        if gain not in [GAIN_LOW, GAIN_MED, GAIN_HIGH, GAIN_MAX]:
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
        if integration_time not in [INTEGRATIONTIME_100MS, INTEGRATIONTIME_200MS,
                            INTEGRATIONTIME_300MS, INTEGRATIONTIME_400MS,
                            INTEGRATIONTIME_500MS, INTEGRATIONTIME_600MS]:
            raise ValueError("Invalid integration time setting.")
        self.sensor.integration_time = integration_time
        
    # ----------------------------------------------------------------
    # AUTOMATIC GAIN ADJUSTMENT
    # ----------------------------------------------------------------   
    def auto_gain_adjust(self, lux: float) -> None:
        """
        Automatically adjusts sensor gain and integration time based on the current lux value.
        This improves accuracy in varying light conditions without requiring user input.
        """
        gain = self.get_gain()
        integration = self.get_integration_time()
        
        # Definitions for adjustment thresholds
        if lux < 10:
            desired_gain = GAIN_MAX
            desired_time = INTEGRATIONTIME_600MS
        elif lux < 100:
            desired_gain = GAIN_HIGH
            desired_time = INTEGRATIONTIME_400MS
        elif lux < 1000:
            desired_gain = GAIN_MED
            desired_time = INTEGRATIONTIME_300MS
        elif lux < 40000:
            desired_gain = GAIN_LOW
            desired_time = INTEGRATIONTIME_200MS
        else:
            desired_gain = GAIN_LOW
            desired_time = INTEGRATIONTIME_100MS
            
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