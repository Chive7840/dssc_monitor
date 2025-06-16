from datetime import datetime
from typing import Optional
from logger.db import SensorDatabase

class SensorLogger:
    def __init__(self, *, db: SensorDatabase) -> None:
        """
        Initializes the SensorLogger with an injected SensorDatabase.
        
        Args:
            db (SensorDatabase): Database instance used for storing readings.
        """
        self.db: SensorDatabase = db
        
    def log_data(
        self,
        *,
        lux: float,
        temperature: float,
        humidity: float,
        timestamp: Optional[str] = None
    )-> None:
        """
        Logs sensor data to the database with an optional timestamp.
        
        Args:
            lux (float): Light intensity value.
            temperature (float): Temperature value in Celsius.
            humidity (float): Relative humidity percentage.
            timestamp (Optional[str]): Optional ISO-formatted timestamp. If not provided current time is used.
        """      
        resolved_timestamp: str = timestamp or datetime.now().isoformat()
        
        sensor_data: dict[str, float | str] = {
            "timestamp": resolved_timestamp,
            "lux": lux,
            "temperature": temperature,
            "humidity": humidity
        }
        
        self.db.insert_data(sensor_data)
        
        print(f"[{resolved_timestamp}] Lux: {lux:.2f}, Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")

    def close(self) -> None:
        """
        Closes the associated database connection.
        """
        self.db.close_conn()