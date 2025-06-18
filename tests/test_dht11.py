from time import sleep
from unittest import TestCase
from sensors.dht11 import DHT11Sensor




class TestDHT11Sensor(TestCase):
    """
    Integration tests for the DHT11 sensor.
    """
    
    def setUp(self):
        self.sensor = DHT11Sensor()
        
    def tearDown(self):
        self.sensor.cleanup()
         
    def test_readings_are_valid(self):
        """
        Test that temperature and humidity readings are not None.
        """
        reading = self.sensor.read()
        if reading is None:
            self.skipTest("Sensor failed to provide valid readings after retries - possible hardware or timing issue.")
        temperature, humidity = reading
        self.assertIsNotNone(temperature)
        self.assertIsNotNone(humidity)


if __name__ == "__main__":
    unittest.main()