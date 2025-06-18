from unittest import TestCase
import os
from database.db import SensorDatabase
from logger.sensor_logger import SensorLogger
from datetime import datetime


class TestSensorLogging(TestCase):
    """
    Unit tests for the SensorLogger and SensorDatabase integration.
    """
    
    
    def setUp(self):
        """
        Setup: Create test DB and logger instance
        """
        self.test_db_path = "test_logger.db"
        self.db = SensorDatabase(db_path=self.test_db_path)
        self.logger = SensorLogger(db_path=self.test_db_path)
        
        # Clear tables
        self.db.cursor.execute(f"DELETE FROM {SensorDatabase.get_sensor_table_name()};")
        self.db.cursor.execute(f"DELETE FROM {SensorDatabase.get_cell_output_table_name()};")
        self.db.conn.commit()
        
        
    def tearDown(self):
        """
        Teardown: Clean up DB file and connections
        """
        self.db.close_conn()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
    def test_insert_retrieve(self):
        """
        Test full insert and fetch for sensor_data
        """
        sample_data = {
            "timestamp": "2025-06-12T10:00:00",
            "lux": 123.45,
            "temperature": 22.1,
            "humidity": 56.7
        }
        self.logger.log_data(**sample_data)
        
        result = self.db.conn.execute(f"SELECT * FROM {SensorDatabase.get_sensor_table_name()};").fetchall()
        
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], sample_data["timestamp"])
        self.assertAlmostEqual(row[1], sample_data["lux"])
        self.assertAlmostEqual(row[2], sample_data["temperature"])
        self.assertAlmostEqual(row[3], sample_data["humidity"])
        
    def test_logger_delegates_to_db(self):
        """
        Test that SensorLogger logs through SensorDatabase
        """
        self.logger.log_data(
            timestamp="2025-06-12T12:00:00",
            lux=123.45,
            temperature=22.1,
            humidity=56.7
        )
        
        result = self.db.conn.execute(f"SELECT * FROM {SensorDatabase.get_sensor_table_name()};").fetchone()
        
        self.assertEqual(result[0], "2025-06-12T12:00:00")
        self.assertAlmostEqual(result[1], 123.45) 	# lux
        self.assertAlmostEqual(result[2], 22.1)
        self.assertAlmostEqual(result[3], 56.7)
        
if __name__ == "__main__":
    unittest.main()