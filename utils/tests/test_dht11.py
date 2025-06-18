from time import sleep
import unittest
from sensors.dht11 import DHT11Sensor

def run_dht11_test(unittest.TestCase):
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
        for _ in range(5):
            temperature, humidity = self.sensor.read()
            self.assertIsNotNone(temperature, "Temperature reading is None")
            self.assertIsNotNone(humidity, "Humidity reading is None")
            self.assertIsInstance(temperature, (int, float), "Temperature is not numeric")
            self.assertIsInstance(humidity, (int, float), "Humidity is not numeric")
            sleep(2)

if __name__ == "__main__":
    run_dht11_test()