import sqlite3
from typing import Optional, List, Dict
from pathlib import Path
from logger.db import SensorDatabase

class SensorDataReader:
    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initializes the SensorDataReader with a path to the SQLite database.
        If no path is provided, the class-level default from SensorDatabase is used.
        
        Args:
            db_path (Optional[str]): Path to the SQLite database file.
        """
        resolved_path = db_path or SensorDatabase.get_db_path()
        self.conn = sqlite3.connect(resolved_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
    def get_all_data(self) -> Optional[Dict]:
        """
        Retrieves all records from the sensor_data table.
        
        Returns:
            List[Dict]: A list of all sensor readings as dictionaries.
        """
        query = "SELECT * FROM sensor_data ORDER BY timestamp ASC;"
        self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_latest_entry(self) -> List[Dict]:
        """
        Retrieves the most recent sensor reading.
        
        Returns:
            Optional[Dict]: The most recent row, or None if empty.
        """
        query = "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1;"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_data_between(self, start_iso: str, end_iso: str) -> List[Dict]:
        """
        Retrieves sensor readings within the specified timestamp range.
        
        Args:
            start_iso (str): Start timestamp (inclusive) in ISO format.
            end_iso (str): End timestamp (inclusive) in ISO format.
            
        Returns:
            List[Dict]: Matching records ordered chronologically.
        """
        query = """
            SELECT * FROM sensor_data
            WHERE timestamp BETWEEN ? and ?
            ORDER BY timestamp ASC;
        """
        self.cursor.execute(query, (start_iso, end_iso))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def close(self) -> None:
        """
        Closes the SQLite connection.
        """
        self.conn.close()