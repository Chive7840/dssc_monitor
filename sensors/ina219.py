from adafruit_ina219 import INA219
from adafruit_bus_device.i2c_device import I2CDevice
import board
import busio
from typing import Optional


class INA219Sensor:
    """-- Represents a single INA219 sensor instance --"""
    
    def __init__(self, i2c_bus: busio.I2C, address: int):
        """-- Initialize INA219 sensor at a specifc I2C address --"""
        self.address = address
        self.device = INA219(i2c_bus, address)
        
    def read_voltage(self) -> float:
        """-- Read bus voltage in volts. --"""
        return round(self.device.bus_voltage, 3)
    
    def read_current(self) -> float:
        """-- Read current in milliamps. --"""
        return(self.device.current, 3)
    
    def read_power(self) -> float:
        """-- Read power in milliwatts. --"""
        return round(self.device.power, 3)
    
class INA219Manager:
    """-- Manages multiple INA219 sensors with distinct addresses. --"""
    
    def __init__(self, addresses: list[int]):
        """-- Initialize I2C bus and each sensor on its address --"""
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.sensors = [
            INA219Sensor(self.i2c_bus, addr)
            for addr in addresses
        ]
    
    def read_all(self) -> list[dict]:
        """-- Read telemetry from all attached INA219 sensors --"""
        readings = []
        for idx, sensor in enumerate(self.sensors):
            readings.append({
                "cell_id": idx + 1,
                "voltage": sensor.read_voltage(),
                "current": sensor.read_current(),
                "power": sensor.read_power()
            })
        return readings
    
    def close(self) -> None:
        # No close method required for I2C, but provided for interface symmetry
        pass