from datetime import datetime
from typing import Optional, Dict
from database.db import SensorDatabase

class SensorLogger:
    """
    SensorLogger handles timestamped data logging into appropriate database tables
    """
    
    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initializes the SensorLogger with a SensorDatabase instance.
        
        Args:
            db_path (Optional[str]): Optional path to the SQLite database file.
        """
        self.db = SensorDatabase(db_path=db_path)
        
    def log_data(
        self,
        lux: float,
        temperature: float,
        humidity: float,
        timestamp: Optional[str] = None
    )-> None:
        """
        Logs sensor data to the database with an optional timestamp.
        
        Args:
            lux (float): Light intensity reading from TSL2591.
            temperature (float): Temperature in Celsius from DHT11.
            humidity (float): Relative humidity percentage from DHT11.
            timestamp (Optional[str]): Optional ISO-8 timestamp. Auto-generated if not provided.
        """      
        resolved_timestamp: str = timestamp or datetime.now().isoformat()
        record: Dict[str, float | str] = {
            "timestamp": resolved_timestamp,
            "lux": lux,
            "temperature": temperature,
            "humidity": humidity
        }
        self.db.insert_data(record)
        
    def log_cell_output(
        self,
        cell_id: int,
        data: Dict[str, float],
        timestamp: Optional[str] = None
    ) -> None:
        """
        Logs DSSC electrical data (voltage, current, power).
        
        Args:
            cell_id(int): Unique ID for the cell.
            data (Dict[str, float]): Sensor reading from INA219.
            timestamp (Optional[str]): Optional ISO-8 timestamp.
        """
        resolved_timestamp: str = timestamp or datetime.now().isoformat()
        self.db.insert_cell_output(cell_id=cell_id, reading=data, timestamp=resolved_timestamp)
        

    def close(self) -> None:
        """
        Closes the associated database connection.
        """
        self.db.close_conn()