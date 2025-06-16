from sensors.tsl2591 import TSL2591Sensor
import time

def run_tsl2591_test():
    sensor = TSL2591Sensor()
    print("Starting TSL2591 sensor test...")
    
    for _ in range(5):
        lux = sensor.read_lux()
        print(f"Ambient Light (Lux): {lux:.2f}")
        time.sleep(1)
        
if __name__ == "__main__":
    run_tsl2591_test()