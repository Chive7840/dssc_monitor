from sensors.tsl2591 import TSL2591Sensor
from sensors.dht11 import DHT11Sensor
from logger.sensor_logger import log_sensor_data
from logger.db import SensorDatabase
from time import sleep

def main() -> None:
    # Initialize sensors and logger
    tsl_sensor: TSL2591Sensor = TSL2591Sensor()
    dht_sensor: DHT11Sensor = DHT11Sensor(pin=17) 	# Adjust pin as needed
    
    db: SensorDatabase = SensorDatabase.get_db_path()
    logger: SensorLogger = SensorLogger(db=db)
    
    print("[INFO] Starting live sensor logging. Press CTRL+C to stop logging.")
    
    try:
        while True:
            try:
                lux: float = tsl_sensor.read_lux()
                temperature: float
                humidity: float
                temperature, humidity = dht_sensor.read()
                
                # Guards against invalid DHT11 readings
                if temperature is not None and humidity is not None:
                    logger.log(
                        lux = lux,
                        temperature = temperature,
                        humidity = humidity
                    )
                else:
                    print("[WARN] DHT11 read failed. Skipping DHT11 reading.")
                
                sleep(10) # log every 10 seconds (adjustable)
                
            except RuntimeError as err:
                print(f"Sensor read error: {err}")
            
    except KeyboardInterrupt:
        print("\n[INFO] Logging interrupted by user.")

    finally:
        logger.close()
        print("[INFO] Sensor logging stopped and database closed.")

if __name__ == "__main__":
    main()
    