from sensors.tsl2591 import TSL2591Sensor
from sensors.dht11 import DHT11Sensor
from sensors.ina219 import INA219Manager
from logger.sensor_logger import SensorLogger
from time import sleep


def setup_sensors():
    """-- Initializes all sensors --"""
    tsl_sensor = TSL2591Sensor()
    dht_sensor = DHT11Sensor()
    ina_sensors = [INA219Sensor(address=addr) for addr in [0x40, 0x41, 0x44]]
    return tsl_sensor, dht_sensor, ina_sensors



def main():
    """-- Executes main logging loop for all sensors --"""
    logger = SensorLogger()
    tsl_sensor, dht_sensor, ina_sensors = setup_sensors()

    try:
        while True:
            # -- Light sensor (TSL2591) --
            try:
                lux = tsl_sensor.read_lux()
                tsl_sensor.auto_adjust(lux)
                print(f"[LOG] Light intensity: {lux:.2f}")
                logger.log_data(lux=lux)
            except Exception as err:
                print(f"[ERROR] Failed to read TSL2591: {err}")
            
            # -- Humidity & Temperature sensor (DHT11) --
            try:
                temp, humidity = dht_sensor.read()
                print(f"[LOG] Temp: {temp:.1f}°C | Humidity: {humidity:.1f}%")
                logger.log_data(temp=temp, humidity=humidity)

            except Exception as err:
                print(f"[ERROR] Failed to read DHT11: {err}")
                
            # -- Voltage/current sensors (INA219) --
            for idx, sensor in enumerate(ina_sensors, start=1):
                try:
                    voltage = sensor.read_voltage()
                    current = sensor.read_current()
                    power = sensor.read_power()
                    print(f"[LOG] Cell{idx}: Voltage={voltage:.3f}V, Current={current:.3f}mA P={power:.2f}mW")
                    logger.log_cell_output(cell_id=idx, voltage=voltage, current=current, power=power)

                except Exception as err:
                    print(f"[ERROR] Failed to read INA219 sensor {idx}: {err}")
                    
            sleep(5)
            
    except KeyboardInterrupt:
        print("[ERROR] Logging interrupted by user.\nTerminating...")
    finally:
        logger.close()

if __name__ == "__main__":
    main()