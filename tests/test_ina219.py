"""
Integration test for INA219 sensors. This is a real sensor test, not a mock sensor test
"""

from unittest import TestCase
from sensors.ina219 import INA219Manager




class TestINA219(TestCase):
    """
    Integration tests using live INA219 sensors.
    """
    
    def setUp(self):
        self.manager = INA219Manager()
        
    def test_sensors_return_valid_readings(self):
        """
        Ensure all INA219 sensors return numeric voltage, current, and power.
        """
        
        readings = self.manager.read_all()
        self.assertEqual(len(readings), 3, "Expected 3 sensors to return readings")
        
        for entry in readings:
            with self.subTest(cell_id=entry["cell_id"]):
                self.assertIsInstance(entry["voltage"], float)
                self.assertIsInstance(entry["current"], float)
                self.assertIsInstance(entry["power"], float)
                
                # Optional sanity checks
                self.assertGreaterEqual(entry["voltage"], 0.0)
                self.assertGreaterEqual(entry["current"], 0.0)
                self.assertGreaterEqual(entry["power"], 0.0)
                
    def tearDown(self):
        self.manager.close()
        


if __name__ == "__main__":
    unittest.main()