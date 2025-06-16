import unittest
import os
import sqlite3
from datetime import datetime, timedelta

from logger.data_access import SensorDataReader
from logger.db import SensorDatabase

TEST_DB = "test_sensor_data.db"

class TestSensorDataReader(unittest.TestCase):
    def setUp(self) -> None:
        # Ensure a fresh database file
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        
        self.db = SensorDatabase(db_path=TEST_DB)
        now = datetime.now()
        
        self.sample_data = [
            {
                "timestamp": (now - timedelta(seconds=30)).isoformat(),
                "lux": 123.4,
                "temperature": 22.1,
                "humidity": 45.0,
            },
            {
                "timestamp": (now - timedelta(seconds=10)).isoformat(),
                "lux": 456.7,
                "temperature": 23.5,
                "humidity": 50.2,
            },
            {
                "timestamp": now.isoformat(),
                "lux": 789.0,
                "temperature": 24.3,
                "humidity": 55.6,
            },
        ]
        
        for row in self.sample_data:
            self.db.insert_data(row)
            
        self.reader = SensorDataReader(db_path=TEST_DB)
        
    def tearDown(self) -> None:
        self.reader.close()
        self.db.close_conn()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        
    def test_get_all_data_returns_correct_count(self):
        result = self.reader.get_all_data()
        self.assertEqual(len(result), len(self.sample_data))
        
    def test_get_latest_entry_returns_most_recent(self):
        latest = self.reader.get_latest_entry()
        expected = self.sample_data[-1]
        self.assertEqual(latest["timestamp"], expected["timestamp"])
        
    def test_get_data_between_filters_correctly(self):
        start = self.sample_data[0]["timestamp"]
        end = self.sample_data[1]["timestamp"]
        
        result = self.reader.get_data_between(start, end)
        # Should include both sample[0] and sample[1]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["timestamp"], self.sample_data[0]["timestamp"])
        self.assertEqual(result[1]["timestamp"], self.sample_data[1]["timestamp"])
        
if __name__ == "__main__":
    unittest.main()