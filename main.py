from sensors.tsl2591 import TSL2591Sensor
from sensors.dht11 import DHT11Sensor
from sensors.ina219 import INA219Manager
from logger.sensor_logger import SensorLogger
from logger.db import SensorDatabase
from time import sleep


def setup_sensors():
    """-- Initializes all sensors --"""
    return {
        "ambient": TSL2591Sensor(),
        "dht": DHT11Sensor(),
        "cell_a": INA219Sensor(i2c_addr=0x40),
        "cell_b": INA219Sensor(i2c_addr=0x41),
        "cell_c": INA219Sensor(i2c_addr=0x44),
    }



def main():
    """-- Executes main logging loop for all sensors --"""
    sensors = setup_sensors()
    logger = SensorLogger()

    try:
        while True:
            # -- Read from TSL2591 --
            try:
                lux = sensors["ambient"].read_lux()
                logger.log_data("ambient_light", {"lux": lux})
                print(f"[Ambient] Lux: {lux:.2f}")
            except Exception as err:
                print(f"[Ambient Sensor Error] {err}")
            
            # -- Read from DHT11 --
            try:
                temp, humidity = sensors["dht"].read()
                logger.log_data("temperature_humidity", {
                    "temperature": temp,
                    "humidity": humidity
                })
                print(f"[DHT11] Temp: {temp:.1f}°C | Humidity: {humidity:.1f}%")
            except Exception as err:
                print(f"[DHT11 Sensor Error] {err}")
                
            # -- Read from each INA219 cell --
            for cell_key in ("cell_a", "cell_b", "cell_c"):
                try:
                    voltage = sensors[cell_key].read_bus_voltage()
                    current = sensors[cell_key].read_current()
                    power = sensors[cell_key].read_power()
                    logger.log_data("cell_output", {
                         "cell_id": cell_key.upper(),
                         "voltage": voltage,
                         "current": current,
                         "power": power
                    })
                    print(f"[{cell_key.upper()}] V={voltage:.2f}V I={current:.2f}mA P={power:.2f}mW")
                except Exception as err:
                    print(f"[{cell_key.upper()} Sensor Error] {err}")
                    
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("Terminating...")


if __name__ == "__main__":
    main()