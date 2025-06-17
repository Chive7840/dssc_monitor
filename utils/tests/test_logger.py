import unittest
import os
from logger.db import SensorDatabase
from logger.sensor_logger import SensorLogger
from datetime import datetime


class TestSensorLogging(unittest.TestCase):
    
    
    def setUp(self):
        """-- Setup: Create test DB and logger instance --"""
        self.test_db_path = "test_logger.db"
        self.db = SensorDatabase(db_path=self.test_db_path)
        self.logger = SensorLogger(db_path=self.test_db_path)
        
        # Clear tables
        self.db.cursor.execute(f"DELETE FROM {SensorDatabase._SENSOR_TABLE};")
        self.db.cursor.execute(f"DELETE FROM {SensorDatabase._CELL_OUTPUT_TABLE};")
        self.db.conn.commit()
        
        
    def tearDown(self):
        """-- Teardown: Clean up DB file and connections --"""
        self.db.close_conn()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
    def test_insert_retrieve(self):
        """-- Test full insert and fetch for sensor_data --"""
        sample_data = {
            "timestamp": "2025-06-12T10:00:00",
            "lux": 123.45,
            "temperature": 22.1,
            "humidity": 56.7
        }
        self.logger.log_data(**sample_data)
        result = self.db.conn.execute(f"SELECT * FROM {SensorDatabase._SENSOR_TABLE};").fetchall()
        self.assertEqual(len(result), 1)
        
    def test_logger_delegates_to_db(self):
        """-- Test that SensorLogger logs through SensorDatabase --"""
        self.logger.log_data(
            lux=150.0,
            temperature=23.5,
            humidity=55.0,
            timestamp="2025-06-12T12:00:00"
        )
        result = self.db.conn.execute(f"SELECT * FROM {SensorDatabase._SENSOR_TABLE};").fetchone()
        self.assertAlmostEqual(result[1], 150.0) 	# lux
        
if __name__ == "__main__":
    unittest.main()