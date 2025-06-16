import sqlite3
from pathlib import Path
from typing import Dict


class SensorDatabase:
    _DEFAULT_DB_PATH = "sensor_data.db"
    
    def __init__(self, db_path="sensor_data.db") -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        self._setup()
        
    def _setup(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                timestamp TEXT NOT NULL,
                lux REAL NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL
            );
        """)
        self.conn.commit()

        
    def insert_data(self, sensor_data: Dict[str, float | str]) -> None:
        self.cursor.execute(
            """
            INSERT INTO sensor_data (timestamp, lux, temperature, humidity)
            VALUES (?, ?, ?, ?);
            """,
            (
                sensor_data["timestamp"],
                sensor_data["lux"],
                sensor_data["temperature"],
                sensor_data["humidity"]
            )
        )
        self.conn.commit()
        
    def close_conn(self) -> None:
        self.conn.close()
        
    @classmethod
    def get_db_path(cls) -> str:
        """
        Returns the default database path used by the SensorDatabase class.
        """
        return cls._DEFAULT_DB_PATH