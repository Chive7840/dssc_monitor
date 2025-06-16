import unittest
from logger.db import SensorDatabase
from logger.sensor_logger import SensorLogger
from datetime import datetime
from typing import Any

class TestSensorLogging(unittest.TestCase):
    
    def setUp(self) -> None:
        # Uses in-memory SQLite DB (won't persist to disk)
        self.db: SensorDatabase = SensorDatabase(":memory:")
        self.logger: SensorLogger = SensorLogger(db=self.db)
        
    def test_tear_down(self) -> None:
        self.db.close_conn()
        
    def test_insert_retrieve(self) -> None:
        sample_data: dict[str, float | str] = {
            "timestamp": datetime.now().isoformat(),
            "lux": 123.45,
            "temperature": 22.1,
            "humidity": 56.7
        }
        
        self.db.insert_data(sample_data)
        
        self.db.cursor.execute("SELECT * FROM sensor_data;")
        row: tuple[Any, ...] = self.db.cursor.fetchone()
        
        self.assertIsNotNone(row)
        self.assertEqual(float(row[1]), sample_data["lux"])
        self.assertEqual(float(row[2]), sample_data["temperature"])
        self.assertEqual(float(row[3]), sample_data["humidity"])
        
    def test_logger_delegates_to_db(self) -> None:
        self.logger.log_data(
            lux = 150.0,
            temperature = 23.5,
            humidity = 55.0
        )
        
        self.db.cursor.execute("SELECT COUNT(*) FROM sensor_data;")
        count: int = self.db.cursor.fetchone()[0]
        self.assertEqual(count, 1)
        
if __name__ == "__main__":
    unittest.main()