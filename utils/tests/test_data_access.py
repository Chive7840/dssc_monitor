import unittest
import os
from typing import List, Dict
from datetime import datetime, timedelta
from logger.data_access import SensorDataReader
from logger.db import SensorDatabase


class TestSensorDataReader(unittest.TestCase):
    """
    Test suite for validating functionality of SensorDataReader
    with both sensor and cell output tables.
    """
    
    def setUp(self) -> None:
        """
        Setup in-memory test DB and seed sample data
        """
        self.test_db_path = "test_sensor_data.db"
        self.db = SensorDatabase(db_path=self.test_db_path)
        self.reader = SensorDataReader(db_path=self.test_db_path)
        
        # Clear existing tables before each test
        self.db.cursor.execute(f"DELETE FROM {SensorDatabase._SENSOR_TABLE};")
        self.db.cursor.execute(f"DELETE FROM {SensorDatabase._CELL_OUTPUT_TABLE};")
        self.db.conn.commit()
        
        # Seed sensor_data
        self.sample_data: List[Dict] = [
            {
                "timestamp": (datetime.now() - timedelta(minutes=i)).isoformat(),
                "lux": 100.0 + i,
                "temperature": 22.1 + i,
                "humidity": 45.0 + i,
            }
            for i in range(3)
        ]
        for entry in self.sample_data:
            self.db.insert_data(entry)
            
        # Seed cell_output
        self.sample_cell_data: List[Dict] = [
            {
                "timestamp": self.sample_data[i]["timestamp"],
                "cell_id": i,
                "voltage": 0.5 + i,
                "current": 0.01 + i,
                "power": 0.005 + i,
            }
            for i in range(3)
        ]
        for entry in self.sample_cell_data:
            self.db.insert_cell_output(
                cell_id=entry["cell_id"],
                reading={
                    "voltage": entry["voltage"],
                    "current": entry["current"],
                    "power": entry["power"],
                },
                timestamp=entry["timestamp"],
            )
        
    def tearDown(self) -> None:
        """
        Clean up test database and close connections.
        """
        self.reader.close()
        self.db.close_conn()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
    def test_get_all_data_returns_correct_count(self):
        """
        Test get_data_between for both tables returns correct number of records.
        """
        start = self.sample_data[2]["timestamp"]
        end = self.sample_data[0]["timestamp"]
        
        sensor_results = self.reader.get_data_between(
            SensorDatabase._SENSOR_TABLE, start, end
        )        
        cell_results = self.reader.get_data_between(
            SensorDatabase._CELL_OUTPUT_TABLE, start, end
        )
        
        self.assertEqual(len(sensor_results), len(self.sample_data))
        self.assertEqual(len(cell_results), len(self.sample_cell_data))
  
        
    def test_get_latest_entry_returns_most_recent(self):
        """
        Test get_latest_entry returns correct sensor and cell records.
        """
        sensor_entry = self.reader.get_latest_entry(SensorDatabase._SENSOR_TABLE)
        cell_entry = self.reader.get_latest_entry(SensorDatabase._CELL_OUTPUT_TABLE)
        
        self.assertEqual(latest_sensor["timestamp"], self.sample_data[0]["timestamp"])
        self.assertEqual(latest_cell["timestamp"], self.sample_cell_data[0]["timestamp"])
        
    def test_row_to_dict_sensor_type(self):
        """
        Ensure _row_to_dict parses sensor table rows correctly
        """
        test_row = (
            self.sample_data[0]["timestamp"],
            self.sample_data[0]["lux"],
            self.sample_data[0]["temperature"],
            self.sample_data[0]["humidity"],
        )
        result = self.reader._row_to_dict(test_row, "sensor")
        self.assertEqual(result["lux"], self.sample_data[0]["lux"])
        
    def test_row_to_dict_cell_type(self):
        """
        Ensure _row_to_dict parses cell table rows correctly.
        """
        test_row = (
            self.sample_cell_data[0]["timestamp"],
            self.sample_cell_data[0]["cell_id"],
            self.sample_cell_data[0]["voltage"],
            self.sample_cell_data[0]["current"],
            self.sample_cell_data[0]["power"],
        )
        result = self.reader._row_to_dict(test_row, "cell")
        self.assertEqual(result["cell_id"], self.sample_cell_data[0]["cell_id"])
        
    def test_row_to_dict_invalid_type_returns_empty_dict(self):
        """
        Invalid table_type passed to _row_to_dict should return an empty dictionary.
        """
        result = self.reader._row_to_dict((), "invalid_type")
        self.assertEqual(result, {})
        
        
if __name__ == "__main__":
    unittest.main()