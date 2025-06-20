import sqlite3
from pathlib import Path
from typing import Dict, Optional, Any


class SensorDatabase:
    _DEFAULT_DB_PATH = "sensor_data.db"
    _SENSOR_TABLE = "sensor_data"
    _CELL_OUTPUT_TABLE = "cell_output"
    
    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initializes a connection to the SQLite database.
        
        Args:
            db_path (Optional[str]): Path to the SQLite DB file.
                                     Defaults to 'sensor_data.db' if None.
        """
        self.db_path: str = db_path or self._DEFAULT_DB_PATH
        self.conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self._setup()
        
    @classmethod
    def get_sensor_table_name(cls) -> str:
        """
        Returns the name of the general sensor data table.
        """
        return cls._SENSOR_TABLE
    
    @classmethod
    def get_cell_output_table_name(cls) -> str:
        """
        Returns the name of the cell output data table.
        """
        return cls._CELL_OUTPUT_TABLE
        
    def _setup(self) -> None:
        """
        Ensures required tables exist in the database.
        """
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self._SENSOR_TABLE} (
                timestamp 	TEXT 	NOT NULL,
                lux 		REAL,
                temperature REAL,
                humidity 	REAL,
                PRIMARY KEY (timestamp)
            );
        """)
        
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self._CELL_OUTPUT_TABLE} (
                timestamp 	TEXT 	NOT NULL,
                cell_id 	INTEGER NOT NULL,
                voltage 	REAL,
                current 	REAL,
                power		REAL,
                PRIMARY KEY (timestamp, cell_id)
            );
        """)
        self.conn.commit()

        
    def insert_data(self, data: Dict[str, Any]) -> None:
        """
        Inserts a sensor reading (lux, temp, humidity) into the database.
        
        Args:
            data (Dict[str, Any]): Sensor data dictionary.
        """
        self.cursor.execute(
            f"""
            INSERT INTO {self._SENSOR_TABLE} (timestamp, lux, temperature, humidity)
            VALUES (?, ?, ?, ?);
            """,
            (
                data["timestamp"],
                data["lux"],
                data["temperature"],
                data["humidity"],
            )
        )
        self.conn.commit()
        
    def insert_cell_output(self, cell_id: int, reading: Dict[str, float], timestamp: str) -> None:
        """
        Inserts a DSSC output reading into the database.
        
        Args:
            cell_id (int): The identifier for the DSSC (e.g., 1, 2, 3)
            reading (Dict[str, float]): A dictionary with voltage, current, and power.
            timestamp (str): ISO-format timestamp.
        """
        self.cursor.execute(
            f"""
            INSERT INTO {self._CELL_OUTPUT_TABLE} (timestamp, cell_id, voltage, current, power)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                timestamp,
                cell_id,
                reading["voltage"],
                reading["current"],
                reading["power"],
            )
        )
        self.conn.commit()
        
    def close_conn(self) -> None:
        """
        Closes the SQLite database connection.
        """
        self.conn.close()
        