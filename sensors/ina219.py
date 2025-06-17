from adafruit_ina219 import INA219
import board
import busio
from typing import List


class INA219Sensor:
    """
    Represents a single INA219 sensor instance.
    """
    
    def __init__(self, i2c, address: int, cell_id: str):
        """
        Initialize INA219 sensor at a specifc I2C address.
        """
        self.cell_id = cell_id
        self.device = INA219(i2c_bus, address)
        
    def read_voltage(self) -> float:
        """
        Read bus voltage in volts.
        """
        return round(self.device.bus_voltage, 3)
    
    def read_current(self) -> float:
        """
        Read current in milliamps.
        """
        return round(self.device.current, 3)
    
    def read_power(self) -> float:
        """
        Read power in milliwatts.
        """
        return round(self.device.power, 3)
    
    def close(self) -> None:
        """
        Placeholder for future resource cleanup if necessary.
        """
        pass
    
class INA219Manager:
    """
    Manages multiple INA219 sensors with distinct addresses.
    """
    
    def __init__(self):
        """
        Initialize I2C bus and each sensor on its address.
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensors: List[INA219Sensor] = [
            INA219Sensor(self.i2c, address=0x40, cell_id="cell_1"),
            INA219Sensor(self.i2c, address=0x41, cell_id="cell_2"),
            INA219Sensor(self.i2c, address=0x44, cell_id="cell_3")
        ]
    
    def read_all(self) -> List[dict]:
        """
        Read telemetry from all attached INA219 sensors.
        """
        data = []
        for sensor in self.sensors:
            entry = {
                "cell_id": sensor.cell_id,
                "voltage": sensor.read_voltage(),
                "current": sensor.read_current(),
                "power": sensor.read_power()
            }
            data.append(entry)
        return data
    
    def close(self) -> None:
        # No close method required for I2C, but provided for interface symmetry
        pass