"""
Unit test for the TSL2591 ambient light sensor module.
"""

from sensors.tsl2591 import TSL2591Sensor
import unittest



class TestTSL2591Sensor(unittest.TestCase):
    """
    Test suite for verifying functionality of the TSL2591Sensor class.
    """
    
    def setUp(self):
        """
        Initialize the TSL2591 sensor instance before each test.
        """
        self.sensor = TSL2591Sensor()
        
    def tearDown(self):
        """
        Clean up sensor state after each test, if applicable.
        """
        # Placeholder for teardown logic in case it is needed in the future
        pass
    
    def test_lux_reading_returns_float(self):
        """
        Test that read_lux() returns a float.
        """
        lux = self.sensor.read_lux()
        self.assertIsInstance(lux, float, "Lux value should be of type float.")
        
    def test_lux_within_valid_range(self):
        """
        Test that lux reading falls within a plausible sensor range.
        """
        lux = self.sensor.read_lux()
        self.assertGreaterEqual(lux, 0.0, "Lux value should be >= 0.")
        self.assertLess(lux, 200_000.0, "Lux value exceeds expected maximum range.")
        
    def test_auto_gain_adjust_changes_gain_on_low_lux(self):
        """
        Test that auto_gain_adjust increases gain or integration time when lux is low.
        """
        # Simulate low light conditions
        self.sensor.set_gain(self.sensor.GAIN_LOW)
        self.sensor.set_integration_time(self.sensor.INTEGRATION_TIME_100MS)
        
        self.sensor.auto_gain_adjust(0.5) 	# Very dim environment
        gain = self.sensor.get_gain()
        integration_time = self.sensor.get_integration_time()
        
        self.assertTrue(
            gain > self.sensor.GAIN_LOW or integration_time > self.sensor.INTEGRATION_TIME_100MS,
            "Expected gain or integration time to increase under low lux conditions."
        )
        
    def test_auto_gain_adjust_changes_gain_on_high_lux(self):
        """
        Test that auto_gain_adjust decreases gain or integration time when lux is high.
        """
        # Simulate high light conditions
        self.sensor.set_gain(self.sensor.GAIN_MAX)
        self.sensor.set_integration_time(self.sensor.INTEGRATION_TIME_600MS)
        
        self.sensor.auto_gain_adjust(180_000.0)		# Extremely bright environment
        gain = self.sensor.get_gain()
        integration_time = self.sensor.get_integration_time()
        
        self.assertTrue(
            gain < self.sensor.GAIN_MAX or integration_time < self.sensor.INTEGRATION_TIME_600MS,
            "Expected gain or integration time to decrease under high lux conditions."
        )




if __name__ == "__main__":
    run_tsl2591_test()