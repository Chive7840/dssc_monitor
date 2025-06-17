from sensors.tsl2591 import TSL2591Sensor
from sensors.dht11 import DHT11Sensor
from sensors.ina219 import INA219Manager
from logger.sensor_logger import SensorLogger
from logger.db import SensorDatabase
from time import sleep



def main() -> None:
    """-- Executes main logging loop for all sensors --"""
    
    # Initializes sensors
    tsl_sensor = TSL2591Sensor()
    dht_sensor = DHT11Sensor(pin=17)	# Adjust pin number as needed
    ina219_manager = INA219Manager(addresses=[0x40, 0x41, 0x44])	# Update I2C addresses as needed
    logger = SensorLogger()

    LOG_INTERVAL= 60	# seconds
        
    print("[INFO] Starting live sensor logging. Press CTRL+C to stop logging.")
    
    while True:
        lux = tsl_sensor.read_lux()
        temperature, humidity = dht_sensor.read()
        
        logger.log_data(
            lux=lux,
            temperature=temperature,
            humidity=humidity
        )
        
        for reading in ina219_manager.read_all():
            logger.log_cell_output(
                cell_id=reading["cell_id"],
                voltage=reading["voltage"],
                current=reading["current"],
                power=reading["power"]
            )
        
        print("[INFO] Sensor data logged.")
        time.sleep(60)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[INFO] Logging interrupted by user.")
    