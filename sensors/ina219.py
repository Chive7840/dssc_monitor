from adafruit_ina219 import INA219
import board
import busio


class INA219Sensor:
    def __init__(self, address: int = 0x40) -> None:
        self.address = address
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = INA219(self.i2c, address=self.address)
        
    def read(self) -> dict[str, float]:
        """
        Reads voltage, current, and power output from the sensor.
        
        Returns:
            dict[str, float]: Dictionary containing voltage, current, and power.
        """
        return {
            "voltage": round(self.sensor.bus_voltage, 3),
            "current": round(self.sensor.current, 6), 	# Measured in mA
            "power": round(self.sensor.power, 6)		# Measured in mW
        }
    
    def close(self) -> None:
        # No close method required for I2C, but provided for interface symmetry
        pass