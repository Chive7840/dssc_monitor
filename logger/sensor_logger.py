from datetime import datetime
from typing import Optional, Dict, Any
from logger.db import SensorDatabase

class SensorLogger:
    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initializes the SensorLogger with an injected SensorDatabase.
        
        Args:
            db_path (Optional[str]): The path for the database instance used for storing readings.
        """
        self.db = SensorDatabase(db_path=db_path)
        
    def log_data(self, data: Dict[str, Any], timestamp: Optional[str] = None)-> None:
        """
        Logs sensor data to the database with an optional timestamp.
        
        Args:
            data (Dict[str, Any]): Sensor readings
            timestamp (Opional[str]): Optional ISO-8 timestamp.
        """      
        resolved_timestamp: str = timestamp or datetime.now().isoformat()
        
        record = {
            "timestamp": resolved_timestamp,
            "lux": data["lux"],
            "temperature": data["temperature"],
            "humidity": data["humidity"]
        }
        self.db.insert_data(record)
        
    def log_cell_output(self, cell_id: int, data: Dict[str, float], timestamp: Optional[str] = None) -> None:
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