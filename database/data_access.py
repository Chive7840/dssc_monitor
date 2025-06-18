from typing import List, Dict
from logger.db import SensorDatabase

class SensorDataReader:
    """
    Provides access to sensor and DSSC data stored in the SQLite data.
    """
    
    def __init__(self, db_path: str) -> None:
        """
        Initializes the data reader with a given database path.
        
        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db = SensorDatabase(db_path=db_path)
        self.cursor = self.db.cursor
        self.conn = self.db.conn
        
    def get_all_data(self) -> List[Dict]:
        """
        Retrieves all records from the sensor_data table.
        
        Returns:
            List[Dict]: A list of all sensor readings as dictionaries.
        """
        self.cursor.execute(f"SELECT * FROM {SensorDatabase._SENSOR_TABLE};")
        rows = self.cursor.fetchall()
        return [self._row_to_dict(row, "sensor") for row in rows]
    
    def get_all_dssc_data(self) -> List[Dict]:
        """
        Retrieves all DSSC electrical data.
        
        Returns:
            List[Dict]: All rows from the cell_output table.
        """
        self.cursor.execute(f"SELECT * FROM {SensorDatabase._CELL_OUTPUT_TABLE};")
        rows = self.cursor.fetchall()
        return [self._row_to_dict(row, "cell") for row in rows]
    
    def get_latest_entry(self, table: str) -> Dict:
        """
        Retrieves the most recent sensor reading.
        
        Args:
            table (str): Must be either _SENSOR_TABLE or _CELL_OUTPUT_TABLE
        
        Returns:
            Dict: The most recent row, or None if empty.
            
        Raises:
            ValueError: If an invalid table name is provided.
        """
        if table not in {SensorDatabase._SENSOR_TABLE, SensorDatabase._CELL_OUTPUT_TABLE}:
            raise ValueError("Invalid table specified.")
        
        self.cursor.execute(
            f"""
            SELECT * FROM {table}
            ORDER BY timestamp DESC LIMIT 1;
            """
        )
        row = self.cursor.fetchone()
        return self._row_to_dict(row, "sensor" if table == SensorDatabase._SENSOR_TABLE else "cell")
    
    def get_data_between(self, table: str, start: str, end: str) -> List[Dict]:
        """
        Retrieves sensor readings within the specified timestamp range.
        
        Args:
            table (str): Table name to query.
            start (str): Start timestamp (inclusive) in ISO format.
            end (str): End timestamp (inclusive) in ISO format.
            
        Returns:
            List[Dict]: Matching records ordered chronologically.
            
        Raises:
            ValueError: If an invalid table name is provided.
        """
        if table not in {SensorDatabase._SENSOR_TABLE, SensorDatabase._CELL_OUTPUT_TABLE}:
            raise ValueError("Invalid table specified.")
        
        self.cursor.execute(
            f"""
            SELECT * FROM {table}
            WHERE timestamp BETWEEN ? and ?
            ORDER BY timestamp ASC;
            """,
            (start, end),
        )
        rows = self.cursor.fetchall()
        row_type = "sensor" if table == SensorDatabase._SENSOR_TABLE else "cell"
        return [self._row_to_dict(row, row_type) for row in rows]
     
    
    def _row_to_dict(self, row, table_type: str) -> Dict:
        """
        Converts a row tuple into a dictionary based on table type.
        
        Args:
            row (tuple): SQLite row result.
            table_type (str): 'sensor' or 'cell'.
            
        Returns:
            Dict: Structured dictionary of row data.
        """
        
        if table_type == "sensor":
            return {
                "timestamp": row[0],
                "lux": row[1],
                "temperature": row[2],
                "humidity": row[3],
            }
        elif table_type == "cell":
            return {
                "timestamp": row[0],
                "cell_id": row[1],
                "voltage": row[2],
                "current": row[3],
                "power": row[4],
            }
        return {}
    
    
    def close(self) -> None:
        """
        Closes the SQLite connection.
        """
        self.db.close_conn()