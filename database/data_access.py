from typing import List, Dict
from database.db import SensorDatabase
import pandas as pd

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
    
    def show_all_dataframes(self, print_dfs: bool) -> Dict[str, pd.DataFrame]:
        """
        Returns all data from both tables as pandas DataFrames.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with keys 'sensor_data' and 'cell_output'
        """
        sensor_query = f"SELECT * FROM {SensorDatabase.get_sensor_table_name()};"
        cell_query = f"SELECT * FROM {SensorDatabase.get_cell_output_table_name()};"
        
        sensor_df = pd.read_sql_query(sensor_query, self.conn)
        cell_df = pd.read_sql_query(cell_query, self.conn)
        
        if print_dfs:
            print("Sensor Data:")
            print(sensor_df)
            
            print("\nCell Output:")
            print(cell_df)
        
        return {
            "sensor_data": sensor_df,
            "cell_output": cell_df
        }
    
    def export_to_csv(self, sensor_file: str = "./data_output/sensor_data.csv",
                      cell_file: str = "./data_output/cell_output.csv") -> None:
        """
        Exports both tables to CSV files.
        
        Args:
            sensor_file (str): Filename for sensor_data export.
            cell_file (str): Filename for the cell_output export.
        """
        confirm = input("Export current data to CSV before starting? Type 'YES' to confirm: ")
        if confirm.strip().upper() != "YES":
            raise PermissionError("Data export aborted by user.")
        
        dataframes = self.show_all_dataframes(print_dfs=False)
        dataframes["sensor_data"].to_csv(sensor_file, index=False)
        dataframes["cell_output"].to_csv(cell_file, index=False)
        print(f"[EXPORT] Sensor data saved to: {sensor_file}")
        print(f"[EXPORT] Cell output data saved to: {cell_file}")
    
    def clear_all_data(self) -> None:
        """
        Deletes all records from both sensor_data and cell_output tables.
        Intended for resetting the database before an experiment run.
        Requires user confirmation via interactive prompt to proceed.
        
        Raises: PermissionError: If user declines the confirmation prompt.
        """
        
        confirm = input(
            "WARNING: This will permanently delete all dat from 'sensor_data' and 'cell_output'."
            "Type 'YES' to confirm: "
        )
        if confirm.strip().upper() != "YES":
            raise PermissionError("Data deletion aborted by user.")
        
        self.cursor.execute(f"DELETE FROM {SensorDatabase.get_sensor_table_name()};")
        self.cursor.execute(f"DELETE FROM {SensorDatabase.get_cell_output_table_name()};")
        self.conn.commit()
        print("All data successfully deleted.")
    
    def close(self) -> None:
        """
        Closes the SQLite connection.
        """
        self.db.close_conn()