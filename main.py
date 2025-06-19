from sensors.tsl2591 import TSL2591Sensor
from sensors.dht11 import DHT11Sensor
from sensors.ina219 import INA219Sensor
from logger.sensor_logger import SensorLogger
from database.db import SensorDatabase
from database.data_access import SensorDataReader
from time import sleep
import board
import busio


def setup_sensors():
    """
    Initializes all sensors: DHT11, TSL2591, and INA219 array.
    """
    dht_sensor = DHT11Sensor()
    tsl_sensor = TSL2591Sensor()
    
    i2c = busio.I2C(board.SCL, board.SDA)
    addresses = [0x40, 0x41, 0x44]
    cell_ids = ["cell_1", "cell_2", "cell_3"]
    
    ina_sensors = [INA219Sensor(i2c, addr, cid) for addr, cid in zip(addresses, cell_ids)]
    
    return dht_sensor, tsl_sensor, ina_sensors



def main():
    """-- Executes main logging loop for all sensors --"""
    logger = SensorLogger()
    #reader = SensorDataReader("sensor_data.db")		# TODO: Fix hardcoding to be more dynamic
    dht_sensor, tsl_sensor, ina_sensors = setup_sensors()

    try:
        while True:
            data = {}
            
            #reader.show_all_dataframes(True) # Comment out while the program is gathering data.
            
            # -- Light sensor (TSL2591) --
            lux = None
            
            try:
                lux = tsl_sensor.read_lux()
            except Exception as err:
                print(f"[ERROR] Failed to read TSL2591: {err}")
            
            if lux is not None:
                print(f"[LOG] Light intensity: {lux:.2f}")
                data["lux"] = lux    
            
            # -- Humidity & Temperature sensor (DHT11) --
            try:
                result = dht_sensor.read()
                if result:
                    temperature, humidity = dht_sensor.read()
                    print(f"[LOG] Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
                    data["temperature"] = temperature
                    data["humidity"] = humidity
                else:
                    print("[ERROR] DHT11 reading failed after retries.")
            except Exception as err:
                print(f"[ERROR] Failed to read DHT11: {err}")
                
            # -- Only log if all fields are available --
            if all(k in data for k in ("lux", "temperature", "humidity")):
                logger.log_data(
                    lux=data["lux"],
                    temperature=data["temperature"],
                    humidity=data["humidity"]
                )
                
            # -- Voltage/current sensors (INA219) --
            for idx, sensor in enumerate(ina_sensors, start=1):
                try:
                    voltage = sensor.read_voltage()
                    current = sensor.read_current()
                    power = sensor.read_power()
                    print(f"[LOG] Cell{idx}: Voltage={voltage:.3f}V, Current={current:.3f}mA P={power:.2f}mW")
                    logger.log_cell_output(
                        cell_id=f"cell_{idx}",
                        data={
                            "voltage": voltage,
                            "current": current,
                            "power": power
                        }
                    )

                except Exception as err:
                    print(f"[ERROR] Failed to read INA219 sensor {idx}: {err}")
                    
            sleep(30)
            
    except KeyboardInterrupt:
        print("[ERROR] Logging interrupted by user.\nTerminating...")
    finally:
        dht_sensor.cleanup()
        logger.close()

if __name__ == "__main__":
    main()